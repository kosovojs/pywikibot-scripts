import toolforge
import pywikibot, requests, re, os
import pywikibot
from customFuncs import basic_sparql

conn = toolforge.connect('commonswiki_p','analytics')
site = pywikibot.Site('wikidata', 'wikidata')
commonssite = pywikibot.Site('commons', 'commons')
repo = site.data_repository()

prop = 'P18'


#os.chdir(r'projects/vkpai3')

null = ''

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#

sparqlquery = """select ?id ?item {
  ?item wdt:P2494 ?id .
  filter not exists {?item wdt:P18 ?coords .}
}"""

file2 = basic_sparql(sparqlquery)
print(len(file2))
#file2 = eval(open("query(5).json", "r", encoding='utf-8').read())['results']['bindings']
file2 = {str(entry['id']['value']):entry['item']['value'].replace('http://www.wikidata.org/entity/','') for entry in file2}

SQL = '''SELECT page_title, el_to
FROM externallinks
join page on page_id=el_from and page_namespace=6
where el_to like "http://saraksts.mantojums.lv/lv/piemineklu-saraksts%"'''

sqlRES = run_query(SQL)
print(len(sqlRES))

def doUPL(currItem,image):
	item = pywikibot.ItemPage(repo, currItem)
	item.get(get_redirect=True)
	#print(entry)
	
	if item.claims and prop in item.claims: return
	
	imagelink = pywikibot.Link( image.replace('_',' '), source=commonssite, defaultNamespace=6)
	image = pywikibot.FilePage(imagelink)
	
	newclaim = pywikibot.Claim(repo, prop)
	newclaim.setTarget(image)
	item.addClaim(newclaim)

for entry in sqlRES:
	image,url = entry
	image = encode_if_necessary(image)
	url = encode_if_necessary(url)
	
	urlMatch = re.search('piemineklu-saraksts\/(\d+)',url)
	if not urlMatch: continue
	
	url = str(urlMatch.group(1))
	
	if url not in file2: continue
	
	currItem = file2[url]
	
	doUPL(currItem,image)
#