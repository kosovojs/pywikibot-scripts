import pywikibot, re, os

#os.chdir(r'projects/treisijs')

site = pywikibot.Site("wikidata", "wikidata")
site.login()
lvwiki = pywikibot.Site("lv", "wikipedia")

null = ''

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def getdata():
	lvpage = pywikibot.Page(lvwiki,"Vikipēdija:Raksti, kas nav latviešu valodas Vikipēdijā, bet ir visvairāk citu valodu Vikipēdijās")
	text = lvpage.get()
	
	itemlist = []
	
	pattern = "\| ([^\n]+)\n\| ([^\n]+)\n\| ([^\n]+)\n\| ([^\n]+)\n"
	regex = re.compile(pattern)
	
	for match in regex.finditer(text):
	
		secmat = match.group(2)
		itemregex = re.compile("\[\[:d:([^\|]+)\|([^\]]+)\]\]")
		wditem = re.sub(itemregex,r'\1',secmat)
		itemlist.append(str(wditem).strip())
		
	print('Found items: '+ str(len(itemlist)))
		
	return itemlist
	
titles = getdata()#['Q30652','Q24577','Q128904','Q29921']


#@filedata = eval(open('item.json','r', encoding='utf-8').read())['entities']
filedataREZ = open('tresija saraksts_raw201704.txt','w', encoding='utf-8')

#entis = filedata.keys()

object = {}

def doAPI(wditems):
	r = ''
	idlist = '|'.join(wditems)
	r = pywikibot.data.api.Request(site=site, action="wbgetentities", 
									props="sitelinks", ids=idlist,redirects='yes').submit()
									
	#pywikibot.output(r)
	return r
	

def processone(filedata,entity):
	data = filedata[entity]
	#pywikibot.output(data['sitelinks'])
	sitelinks = data['sitelinks']
	#varbūt pēc tam sakārtot alfabētiskā secībā, ja ir saraksts, nevis dict
	newlinks = {wiki:sitelinks[wiki]['title'] for wiki in sitelinks}# if re.match(regexiw,wiki) or wiki in otherwikis]
	#pywikibot.output(newlinks)
	
	return newlinks
	
	#p31claims = data['claims']
#
groupfd=0
for group in chunker(titles,490):
	print(groupfd)
	groupfd += 1
	entis = doAPI(group)['entities']
	entitylist = entis.keys()
	
	for entdata in entitylist:
		object.update({entdata:processone(entis,entdata)})
		
#pywikibot.output(object)
filedataREZ.write(str(object))