import pywikibot, re, requests, os, toolforge
from datetime import date, timedelta
yesterday = date.today() - timedelta(1)
lastday =  yesterday.strftime('%Y/%m/%d')

#os.chdir(r'projects/lv')

LANG_FOR = 'uk'

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]
#

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b
#
def listthem(language):
	biglist = []
	
	apiout = doAPI2(language)
	thelist = apiout['query']['namespaces']
	
	for one in thelist:
		if one!='0':
			biglist.append(thelist[one]['*'])
			if 'canonical' in thelist[one]:
				biglist.append(thelist[one]['canonical'])
		
	thelist1 = apiout['query']['namespacealiases']
	
	for one1 in thelist1:
		biglist.append(one1['*'])
	
	#pywikibot.output(biglist)
	
	return biglist
#


#{"items":[{"project":"en.wikipedia","access":"all-access","year":"2015","month":"10","day":"10","articles":[{"article":"Main_Page","views":18793503,"rank":1}

apipar = {
	"action": "query",
	"format": "json",
	"meta": "siteinfo",
	"siprop": "namespaces|namespacealiases"
}

exclude = {
	'en':{'startswith':('List of'),'exclude':['Main Page']}
}


#

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#

def doSQL(tlistFor,language):
	object = {}
	conn = toolforge.connect(language + 'wiki_p')
	
	groupfd = 0
	for group in chunker(tlistFor,49):
		#print(groupfd)
		groupfd += 1
		group = [i.replace("'", "\\'").replace(' ','_') for i in group]
		query = "select p.page_title as page, count(l.ll_lang) from langlinks l join page p on p.page_id=l.ll_from where p.page_title in ('" + "','".join(group) + "') and p.page_namespace=0 and not exists (select * from langlinks m where l.ll_from=m.ll_from and m.ll_lang=\""+LANG_FOR+"\") group by l.ll_from;"
		query = query.encode('utf-8')
		#print(query)
		try:
			cursor = conn.cursor()
			cursor.execute(query)
			rows = cursor.fetchall()
		except KeyboardInterrupt:
			sys.exit()
		#revids = []
		for row in rows:
			object.update({encode_if_necessary(row[0]).replace('_',' '):encode_if_necessary(row[1])})
	
	return object
#

def removeFromList(list,lang,nspaces):
	excludeAll = exclude[lang]['exclude'] if lang in exclude else []
	excludeStarts = exclude[lang]['startswith'] if lang in exclude else ()
	
	bigmy = {}
	for one in list:
		title = one["article"].replace('_',' ')
		if title.startswith(nspaces): continue
		
		if title.startswith(excludeStarts): continue
		if title in excludeAll: continue
		
		bigmy.update({title:one["views"]})
	#pywikibot.output(bigmy[:10])
	
	return bigmy
#
def doAPI(wditems,language):
	r = ''
	idlist = '|'.join(wditems)
	
	r = pywikibot.data.api.Request(site=pywikibot.Site(language, "wikipedia"), lllimit="250",action="query", 
									format = "json",prop="langlinks", titles=idlist,redirects='no').submit()
	
	#pywikibot.output(r)
	return r
#
def doAPI2(language):
	r = ''
	r = pywikibot.data.api.Request(site=pywikibot.Site(language, "wikipedia"), action="query", 
									format = "json",siprop="namespaces|namespacealiases", meta="siteinfo").submit()
	
	#pywikibot.output(r)
	return r
#

def get_iwlinks(thelist,lang):
	object = {}
	groupfd=0
	
	for group in chunker(thelist,49):
		print(groupfd)
		groupfd += 1
		apires = doAPI(group,lang)
		entis = apires['query']['pages']
		
		if 'continue' in apires:
			pywikibot.output(apires['continue'])
		
		
		for entdata in entis:
			#pywikibot.output(entis[entdata])
			currData = entis[entdata]
			iws = currData["langlinks"] if "langlinks" in currData else []
			doWeNeed = True
			
			for iw in iws:
				if iw['lang']==LANG_FOR:
					doWeNeed = False
					break
			
			if doWeNeed:
				object.update({currData['title']:len(iws)})
	
	return object
#
def one_item_wiki(data,lang):
	return "* [[:{3}:{0}|{0}]] ({1} iw) — {2} skatījumu".format(data[0],data[2],data[1],lang)
#
def get_pageviews(lang):
	url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/'+lang+'.wikipedia.org/all-access/'+yesterday.strftime('%Y/%m/%d')
	res = requests.get(url).json()
	
	return res

def one_language(language):
	ns = tuple(listthem(language))
	
	pgdata = get_pageviews(language)
	#https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2015/10/10
	parsedList = removeFromList(pgdata["items"][0]["articles"],language,ns)
	afterIws = doSQL(list(parsedList),language)
	#pywikibot.output(afterIws)
	
	WantedArticleList = [[f,parsedList[f],afterIws[f]] for f in parsedList if f in afterIws]
	WantedArticleList.sort(key=lambda x: -x[1])
	WantedArticleList = [one_item_wiki(f,language) for f in WantedArticleList][:100]
	
	
	
	#filedataREZ = open('lvinfoboxes-gfdgdfgdfgdf.txt', 'w', encoding='utf-8')
	#filedataREZ.write('\n'.join(WantedArticleList))
	
	return '== {} ==\n'.format(language)+'{{div col|3}}\n'+'\n'.join(WantedArticleList)+'\n{{div col end}}\n'
	
	
#


def main():
	langs = ['en','de','fr','ru','be','pl','lt','et']
	
	forwiki = []
	
	for lang in langs:
		forwiki.append(one_language(lang))
	#
	textFor = 'Datums: '+yesterday.strftime('{{dat|%Y|%m|%d|n|bez}}')+'\n\n'+'\n\n'.join(forwiki)
	
	
	site = pywikibot.Site('lv','wikipedia')
	page = pywikibot.Page(site,'User:Edgars2007/Missing popular2')
	page.text = textFor
	page.save(comment='Bots: atjaunināts', botflag=False, minor=False)
#
main()