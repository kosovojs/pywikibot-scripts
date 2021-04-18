import json
import pywikibot
from urllib import parse
import customFuncs

site = pywikibot.Site("lv", "wikipedia")

sparql_query = """
SELECT distinct ?item ?itemLabel ?sitelinklv ?imdb (SAMPLE(year(min(?time0))) as ?year) (SAMPLE(?mojo) as ?BOM)
		(SAMPLE(?rotten) as ?Rotten) (SAMPLE(?allmovie) as ?Allmovie) (SAMPLE(?metacritic) as ?Metacritic) (COUNT(distinct ?sitelink) as ?sitelinks) ?ids WHERE {
  ?item wdt:P31 wd:Q11424 .
  ?item wdt:P577 ?time0 .
  #FILTER ( ?time0 >= "2013-01-01T00:00:00Z"^^xsd:dateTime ) .
  OPTIONAL { ?item wdt:P345 ?imdb . }
  OPTIONAL { ?item wdt:P1237 ?mojo . }
  OPTIONAL { ?item wdt:P1258 ?rotten . }
  OPTIONAL { ?item wdt:P1562 ?allmovie . }
  OPTIONAL { ?item wdt:P1712 ?metacritic .  }
	?sitelink schema:about ?item .
	?sitelinklv schema:about ?item .
  ?sitelinklv schema:isPartOf <https://lv.wikipedia.org/> .
    
    BIND(IF(!BOUND(?mojo),0,1)+(IF(!BOUND(?allmovie),0,1))+(IF(!BOUND(?rotten),0,1))+(IF(!BOUND(?metacritic),0,1)) as ?ids)
   SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
   }
 }
GROUP BY ?item ?itemLabel ?imdb ?ids ?sitelinklv
having (?ids<4)
ORDER BY DESC(?sitelinks)
limit 400
"""

#file = open("lvwiki-filmu as-missing.json", "r", encoding='utf-8')
#file = file.read()

json_data = customFuncs.basic_sparql(sparql_query)#json.loads(file)

#http://petscan.wmflabs.org/?psid=558762 -> http://petscan.wmflabs.org/?psid=4367607
#latfilmas = open("lat-filmas.txt", "r", encoding='utf-8').read()

def google(film,site,year):
	querytext = film+' '+ year + ' site:' + site
	
	outputlink = '[https://www.google.lv/search?q={} Google]'.format(parse.quote(querytext))
	
	return outputlink

def getnames(namelistsss):
	namelistsss = namelistsss.split('\n')

	names = []

	for line in namelistsss:
		line = line.split('\t')
		if len(line)>1:
			line = line[1]
			#pywikibot.output(line)
			names.append(line)
	#pywikibot.output(names)
	return names

filmstoskip = customFuncs.basic_petscan('4367607')#getnames(latfilmas)
filmstoskip = [f['title'].replace('_',' ') for f in filmstoskip if f['id']!=0]

mydict = []
counter = 0

begin = '{|class="sortable wikitable"\n|-\n! Npk !! Raksts !! Vikidati !! Gads !! IMDb !! BOM !! Rotten Tomatoes !! Allmovie !! Metacritic !! ID skaits\n|-\n'
	
#{"item":"http://www.wikidata.org/entity/Q132689","itemLabel":"Casablanca","sitelinklv":"https://lv.wikipedia.org/wiki/Kasablanka%20%28filma%29","imdb":"tt0034583","year":"1942","BOM":"casablanca","Rotten":"m/1003707-casablanca","Allmovie":"v8482","sitelinks":"78","ids":"3"}
for item in json_data:
	
	article = item['sitelinklv']['value']
	article = article.replace('https://lv.wikipedia.org/wiki/','')
	article=parse.unquote(article).replace('_',' ')
	if article in filmstoskip:
		continue
	
	counter +=1
	
	prop = item['item']['value']
	prop = prop.replace('http://www.wikidata.org/entity/','')
	
	relyear = item['year']['value']
	enlabel = item['itemLabel']['value']
	
	thisrow = "|-\n| %d || [[%s]] || [[:d:%s|%s]] || %s || %s || %s || %s || %s || %s || %s\n" % (counter,article,prop,prop,item['year']['value'],
																							item['imdb']['value'] if 'imdb' in item else '',
																							item['BOM']['value'] if 'BOM' in item else google(enlabel,'boxofficemojo.com',relyear),
																							item['Rotten']['value'] if 'Rotten' in item else '',
																							item['Allmovie']['value'] if 'Allmovie' in item else '',
																							item['Metacritic']['value'] if 'Metacritic' in item else google(enlabel,'metacritic.com/movie',relyear),
																							item['ids']['value'])
	
	mydict.append(thisrow)
	
tosave = begin+''.join(mydict)+"|}"

report_pageE = pywikibot.Page(site,'Dalībnieks:Edgars2007/Filmu ĀS')
report_pageE.text = tosave
report_pageE.save(summary='bots: atjaunināts saraksts', botflag=False, minor=False)