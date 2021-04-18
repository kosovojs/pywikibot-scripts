import pywikibot, re, os, time, mwparserfromhell, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone
from scripts import upload

#Atmaksas stunda
#127 stundas
#Kārtējais pirmais randiņš

conn = toolforge.connect('lvwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__meta_p')
cursor1 = connLabs.cursor()

ensite = pywikibot.Site("en", "wikipedia")
lvsite = pywikibot.Site("lv", "wikipedia")

imgregex = re.compile("^(\s*\|\s*attēls\s*=\s*)$",re.M)

tplnames_lv = ['filmas infokaste','filma']
tplnames_en = ['film infobox','infobox film','infobox japanese film','infobox movie','infobox tamil film','infobox television']

lv_params = ['attēls']
en_params = ['image']

def do_upl(imgname):
	imgname = imgname.replace('_',' ')
	imgname = re.sub('^([Ff]ile|[Ii]mage):','',imgname)
	if '{{!}}' in imgname or '|' in imgname:
		return False
	
	#imgname = re.sub('({{!}}|\|).+$','',imgname)#fixme: paplašinājums
	imgname = re.sub('(<!--.*?-->)','',imgname)
	image = "File:"+imgname
	page = pywikibot.Page(ensite,image)
	#pywikibot.output(page)
	imagePage = pywikibot.FilePage(ensite,image)
	finalTitle = imagePage.title(with_ns=False)
	if imagePage.isRedirectPage():
		finalTitle = imagePage.getRedirectTarget().title(with_ns=False)

	pywikibot.output(imagePage)
	
	desc = "== Avots ==\n[[:en:File:{name}|{name}]]\n\n== Licence ==\n{{{{Filmas plakāts}}}}".format(name=finalTitle)
	
	#url = 'https://upload.wikimedia.org/wikipedia/en/b/b4/Project_X_Poster.jpg'
	
	bot = upload.UploadRobot(url=imagePage.fileUrl(), description=desc,
								 keepFilename=True,
                                 verifyDescription=False, ignoreWarning=True,
                                 targetSite=lvsite)
	bot.run()
	
	return finalTitle


def downloadPhoto(url):
    '''
    Download the photo and store it in a StrinIO.StringIO object.

    TODO: Add exception handling
    '''
	
    imageFile=urllib.request.urlopen(url).read()
	#)
    return io.StringIO(str(imageFile))
	
def getparam(tlobject,params):
	for param in params:
	
		if tlobject.has(param):
			opficmlapa = tlobject.get(param).value.strip()
					
			if opficmlapa!='':
			
				return opficmlapa
				break
		
		#else:
	return False
#
def enwiki(entitle):
	#entitle = getEnWiki(lvarticle)
	
	if not entitle or entitle=='':
		return
	
	page = pywikibot.Page(ensite,entitle)
	pagetext = page.get()
	wikicode = mwparserfromhell.parse(pagetext)
	templates = wikicode.filter_templates()
	
	for tpl in templates:
		name = tpl.name.lower().strip().replace('_',' ')
		if name in tplnames_en:
			image_en = getparam(tpl,en_params)
			if image_en:
				#do upload
				print('image found')
				imgname = do_upl(image_en)
				return imgname
				
			break
#

def pagename(bg):
	bg = re.sub('\s*(\([^\(]+)$','',bg)
	
	return bg
#
def create_redirect(thispage,redirecttitle):
	thispage = thispage.replace('_',' ')
	if not redirecttitle: return 0
	redirecttitle = pagename(redirecttitle.replace('_',' '))
	
	if redirecttitle==thispage: return  0
	
	if redirecttitle=='': return 0
	
	
	redPage = pywikibot.Page(lvsite,redirecttitle)
	
	if redPage.exists(): return 0
	#pywikibot.output('\t'.join([origtitle,partial,variant,"{}{}".format(partial,variant)]))
	redPage.text = "#REDIRECT [[{}]]".format(thispage)
	redPage.save(summary='bots: pāradresācija uz [[{}]]'.format(thispage), botflag=True, minor=False)
#
def lvwikistuff(articleLV,articleEN):
	page = pywikibot.Page(lvsite,articleLV)
	create_redirect(articleLV,articleEN)
	pagetext = page.get()
	
	wikicode = mwparserfromhell.parse(pagetext)
	templates = wikicode.filter_templates()
	
	for tpl in templates:
		name = tpl.name.lower().strip().replace('_',' ')
		if name in tplnames_lv:
			image_lv = getparam(tpl,lv_params)
			if not image_lv:
				#do upload
				print('no image')
				resulting = enwiki(articleEN)
				
				if resulting:
					wikicoddasde = re.sub(imgregex,r'\1 '+resulting,pagetext)
					pywikibot.showDiff(wikicode,wikicoddasde)
					
					page.put(wikicoddasde, "Bots: pievienots attēls")
			
			break
#

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection = conn):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = connection.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#

SQLMAIN = """select orig.page_title, (select m2.ll_title from langlinks m2 where m2.ll_from=orig.page_id and m2.ll_lang="en")
from revision
join page orig on orig.page_id=rev_page and orig.page_is_redirect=0 and orig.page_namespace=0
where rev_timestamp>{} and rev_parent_id=0
and exists (select * from templatelinks t where orig.page_id = t.tl_from AND t.tl_namespace = 10 AND t.tl_title='Filmas_infokaste')
"""

def get_last_run():
	query = "select lastupd from logtable where job='filmBot'"
	query_res = run_query(query,connLabs)
	
	return encode_if_necessary(query_res[0][0])
#
def set_last_run(timestamp):
	query = "UPDATE `logtable` SET lastupd=%s where job='filmBot'"
	
	timeasUTC = "{0:%Y%m%d%H%M%S}".format(timestamp)
	cursor1.execute(query, (timeasUTC))
	connLabs.commit()
#

def get_articles():
	lastRun = "{0:%Y%m%d%H%M%S}".format(get_last_run())
	query_res = run_query(SQLMAIN.format(lastRun),conn)
	
	return [[encode_if_necessary(f[0]),encode_if_necessary(f[1])] for f in query_res]
#
def main():
	#articles= [f for f in filmlist.split('\n') if len(f)>3]#
	#articlelist = ['','']
	thelist = get_articles()
	for article in thelist:
		lvwikistuff(article[0],article[1])
	
	set_last_run(datetime.utcnow())
		
main()