import re, pywikibot, requests
import toolforge
from datetime import datetime

site = pywikibot.Site('et', "wikipedia")
conn = toolforge.connect('etwiki_p')

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(sqlquery):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(sqlquery)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#
def get_quarry_run(page_id):
	url = 'https://quarry.wmflabs.org/query/{}'.format(page_id)
	res = requests.get(url)
	pagetext = res.text
	
	reg = '"qrun_id": (\d+)'
	
	qid = re.search(reg, pagetext)
	
	if qid:
		return qid.group(1)
#
page_prefix = 'User:Edgars2007/Disambigs'

info_pretext = """* Avots: [[quarry:query/{old}]]
* Atjaunināšanas brīdis: {update}
* Kopējais skaits datu atjaunināšanas brīdī: {number}"""

info_header = '<!-- INFO START -->'
info_footer = '<!-- INFO END -->'

list_header = '<!-- LIST START -->'
list_footer = '<!-- LIST END -->'

templates_header = '<!-- TEMPLATES START -->'
templates_footer = '<!-- TEMPLATES END -->'

#lvwikisource = open('lvwikidbrep1.txt', 'r', encoding='utf-8').read()

def getdata(id,run):
	url2 = "https://quarry.wmflabs.org/query/{}/result/latest/{}/json".format(id,run)
	
	url23= requests.get(url2)#.read()
	#print('here1fsdfsd')
	#pywikibot.output(url2.text)

	data = eval(url23.text)["rows"]
	#print('here1fsdfssfsdfd')
	return data
#
"""
def getdataQQQQQ(id,quaryrDun=quaryrun):
	url2 = lvwikisource[int(id)]
	
	return url2
"""
#
def makeupdate(date):
	
	mon = {
		'1':'janvāris',
		'2':'februāris',
		'3':'marts',
		'4':'aprīlis',
		'5':'maijs',
		'6':'jūnijs',
		'7':'jūlijs',
		'8':'augusts',
		'9':'septembris',
		'10':'oktobris',
		'11':'novembris',
		'12':'decembris'
	}
	f = "%Y-%m-%dT%H:%M:%S"
	datetime = date
	#datetime = datetime.now()#datetime.strptime(date, f)
	#print(datetime.timetuple())
	#http://stackoverflow.com/questions/17118071/python-add-leading-zeroes-using-str-format
	
	dateee = "{}. gada {}. {} plkst. {:0>2}:{:0>2}:{:0>2}".format(datetime.year,datetime.day,mon[str(datetime.month)],datetime.hour,datetime.minute,datetime.second)
	
	return dateee
#
dateget = makeupdate(datetime.now())

def gettext(article):
	try:
		page = pywikibot.Page(site,article)
		text = page.get()
	
		return text
	except:
		''
#
def makeReport(tabula):
	#pywikibot.output(finalout)
	
	return finalout
#
def doreplace(text,pretext,header,footer):
	try:
		newtext = re.sub(header + '.*' + footer, header + '\n' + pretext + '\n' + footer, text, flags=re.DOTALL)
	except:
		newtext = ''
	#pywikibot.output(newtext)
	
	return newtext
#
def infotext(lvwikipagetext,number,old,upddate):
	info_pretext2 = info_pretext.format(update=upddate,number=number,old=old)
	return info_pretext2

#
#sdfsd = infotext(lvwikisource,'dsfdsd','12331321')
#lvwikisource2 = open('lvwikidbrep12.txt', 'w', encoding='utf-8')
#lvwikisource2.write(sdfsd)

#raksti ar visv izmantotie aizs att

sql1 = '''SELECT disambigs.page_title, COUNT(DISTINCT links.pl_from) AS direct_links, COUNT(DISTINCT redirects.page_id) AS redirects,
	COUNT(DISTINCT links.pl_from) + COUNT(DISTINCT links_to_redirects.pl_from) AS all_backlinks
	FROM (SELECT * FROM page_props WHERE pp_propname = 'disambiguation') AS disambigs
	JOIN page AS disambigs
		ON disambigs.page_id = pp_page
	JOIN (SELECT * FROM pagelinks WHERE pl_from_namespace = 0) AS links
		ON links.pl_title = disambigs.page_title AND links.pl_namespace = disambigs.page_namespace
	LEFT JOIN page AS redirects
		ON redirects.page_is_redirect = 1 AND redirects.page_id = links.pl_from AND redirects.page_namespace = disambigs.page_namespace
	LEFT JOIN (SELECT * FROM pagelinks WHERE pl_from_namespace = 0) AS links_to_redirects
		ON links_to_redirects.pl_title = redirects.page_title AND links_to_redirects.pl_namespace = redirects.page_namespace
GROUP BY disambigs.page_title
ORDER BY all_backlinks DESC, direct_links DESC, redirects, disambigs.page_title;
'''

def disambigs_with_links(articlesubpage):
	#articlesubpage = 'Raksti ar visvairāk aizsargātajiem attēliem'
	oldquery = '2951'
	
	curtime = makeupdate(datetime.now())
	data = run_query(sql1)#getdata(oldquery,'1')
	fullarticle = page_prefix+'/'+articlesubpage
	thistext = gettext(fullarticle)
	countinst = len(data)
	thistext = infotext(thistext,countinst,oldquery,curtime)[:200]
	
	report = []
	#vispirms jasakarto
	for article in data:
		#page_title	direct_links	redirects	all_backlinks
		article = [encode_if_necessary(f) for f in article]
		lv,direct,reds,all = article
		lv = lv.replace('_',' ')
		
		row = "|-\n| [[{}]] || {} || {} || {}".format(lv,direct,reds,all)
		report.append(row)
	
	#pywikibot.output(report)
	
	header = '{| class="wikitable sortable"\n|-\n!Disambig !! Links to page !! Redirects !! All backlinks'
	table = '\n'.join(report)
	end = '|}'
	
	finalout = header+'\n'+table+'\n'+end
	
	thistext = finalout#doreplace(thistext,finalout,list_header,list_footer)
	page = pywikibot.Page(site,fullarticle)
	page.put(thistext, "update")
	
	return countinst
#
#########################

#lvwiki aizs. attēli - ir Commons
sql2 = '''SELECT p2.page_title, COUNT(p.page_title) FROM page p
INNER JOIN categorylinks c ON p.page_id = c.cl_from AND c.cl_to = 'Täpsustusleheküljed'
# INNER skips pages whose link COUNT IS zero. CHANGE INNER TO LEFT ON the line below IF you also want TO include those:
INNER JOIN pagelinks pl ON p.page_title = pl.pl_title AND p.page_namespace = pl.pl_namespace
join page p2 on pl.pl_from=p2.page_id
# This counts ALL links, including links FROM talk pages TO disambiguation pages. IF you ONLY want TO COUNT
# links FROM the article namespace, THEN remove the # FROM the line below:
AND pl.pl_from_namespace = 0 and p.page_namespace=0
GROUP BY pl.pl_from
having COUNT(p.page_title)>2
ORDER BY COUNT(p.page_title) DESC;
'''

sql3 = '''SELECT p2.page_title, COUNT(p.page_title) FROM page p
INNER JOIN categorylinks c ON p.page_id = c.cl_from AND c.cl_to = 'Täpsustusleheküljed'
# INNER skips pages whose link COUNT IS zero. CHANGE INNER TO LEFT ON the line below IF you also want TO include those:
INNER JOIN pagelinks pl ON p.page_title = pl.pl_title AND p.page_namespace = pl.pl_namespace
join page p2 on pl.pl_from=p2.page_id
# This counts ALL links, including links FROM talk pages TO disambiguation pages. IF you ONLY want TO COUNT
# links FROM the article namespace, THEN remove the # FROM the line below:
AND pl.pl_from_namespace = 10 and p.page_namespace=0
GROUP BY pl.pl_from
ORDER BY COUNT(p.page_title) DESC;
'''

def pages_with_links(articlesubpage):
	#articlesubpage = 'Raksti ar visvairāk aizsargātajiem attēliem'
	oldquery = '4176'
	curtime = makeupdate(datetime.now())
	
	fullarticle = page_prefix+'/'+articlesubpage
	thistext = gettext(fullarticle)
	
	##############first section
	data = run_query(sql2)#getdata(oldquery,'1')
	countinst = len(data)
	thistext = infotext(thistext,countinst,oldquery,curtime)[:200]
	
	report = []
	for article in data:
		article = [encode_if_necessary(f) for f in article]
		lv,all = article
		lv = lv.replace('_',' ')
		
		row = "|-\n| [[{}]] || {}".format(lv,all)
		report.append(row)
	
	header = '{| class="wikitable sortable"\n|-\n! Title !! Links'
	table = '\n'.join(report)
	end = '|}'
	
	finalout = header+'\n'+table+'\n'+end
	
	thistext = finalout#doreplace(thistext,finalout,list_header,list_footer)
	
	##############second section
	data2 = run_query(sql3)#getdata(oldquery,'2')
	
	report2 = []
	for article2 in data2:
		article2 = [encode_if_necessary(f) for f in article2]
		lv1,all1 = article2
		dispenserlink = "http://dispenser.homenet.org/~dispenser/cgi-bin/dab_solver.py?page=en:Template:{}&commonfixes=on".format(lv1)
		lv1 = lv1.replace('_',' ')
		
		row1 = "|-\n| [[Template:{0}|{0}]] || {1} || [{2} Dab solver]".format(lv1,all1,dispenserlink)
		report2.append(row1)
	
	header1 = '{| class="wikitable sortable"\n|-\n! Title !! Saišu skaits !! Dabsolver'
	table1 = '\n'.join(report2)
	end1 = '|}'
	
	finalout1 = header1+'\n'+table1+'\n'+end1
	
	thistext = doreplace(thistext,finalout1,templates_header,templates_footer)
	
	page = pywikibot.Page(site,fullarticle)
	page.put(thistext, "upd")
	
	return countinst
#

latvian = {
	'ā':'a',
	'ē':'e',
	'ī':'i',
	'ū':'u',
	'Ā':'A',
	'Ē':'E',
	'Ī':'I',
	'Ū':'U',
	##
	'Č':'Cz',
	'Ģ':'Gz',
	'Ķ':'Kz',
	'Ļ':'Lz',
	'Ņ':'Nz',
	'Š':'Sz',
	'Ž':'Zz'
	
}

def fun(v):
	name = v[0]
	
	for repl in latvian:
		name = name.replace(repl,latvian[repl])
	
	#pywikibot.output(name)
	return (name,-v[1])#
#
def maintableD(data):
	data.sort(key=fun)
	artcc = 'User:edgars2007/Disambigs'
	rows = []
	for it in data:
		subp,number = it
		row = "|-\n| [[{main}/{lv}|{lv}]] || {c}".format(main=page_prefix,lv=subp,c=number)
		rows.append(row)
		
	header = '{| class="sortable wikitable"\n|-\n! Atskaite !! Kopējais skaits'
	table = '\n'.join(rows)
	end = '|}'
	
	finalout = 'Atjaunināts: ' + dateget + '\n\n' + header+'\n'+table+'\n'+end
	
	thistext = gettext(artcc)
	thistext = doreplace(thistext,finalout,list_header,list_footer)
	
	page = pywikibot.Page(site,artcc)
	#page.put(thistext, "Bots: atjaunināts")
	
	page.text = thistext
	page.save(summary='update', botflag=False, minor=False)
#

def main():
	maintable = []
	##########
	rep1_articlesubpage = 'Disambigs with links'
	rep1 = disambigs_with_links(rep1_articlesubpage)
	maintable.append([rep1_articlesubpage,rep1])
	##########
	rep2_articlesubpage = 'Pages with links to disambigs'
	rep2 = pages_with_links(rep2_articlesubpage)
	maintable.append([rep2_articlesubpage,rep2])
	##########################
	#maintableD(maintable)
	#############
	#fileesss = open('dbresp1.txt','w', encoding='utf-8')
	#fileesss.write(str(maintable))
	
	
#
main()

#filee = eval(open('quarry-12777-dr-images-lvwiki-run163830.json','r', encoding='utf-8').read())['rows']
#articlesWithMostusedfairuse(filee)