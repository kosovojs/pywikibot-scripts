import requests, os
from bs4 import BeautifulSoup

'''
SELECT ?item ?id (SAMPLE(?enwiki) AS ?enwiki) (COUNT(?wikisourceSitelink) as ?sitelinks) WHERE {
	?item wdt:P1146 ?id .
  ?wikisourceSitelink schema:isPartOf [ wikibase:wikiGroup "wikipedia" ];
                      schema:inLanguage ?wikisourceLanguage;
                      schema:about ?item.
  filter not exists {  ?commons_sitelink schema:about ?item; schema:isPartOf <https://lv.wikipedia.org/> .}
  optional {  ?enwiki schema:about ?item; schema:isPartOf <https://en.wikipedia.org/> .}
	#SERVICE wikibase:label { bd:serviceParam wikibase:language "en,de,fr,pl,ru" }
}
group by ?item ?id
ORDER BY DESC(?sitelinks)
'''

def make_soup(data):
	#req = requests.get(url)
   # html = urllib2.urlopen(req)
	return BeautifulSoup(data, 'html.parser')

def getURL(url):
	get = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'})
	res = get.text

	return res

def getAllLinks():
	allData = getURL('https://www.iaaf.org/competitions/iaaf-world-championships/iaaf-world-athletics-championships-doha-2019-6033/timetable/byday')

	fileData = make_soup(allData)

	tableWrapper = fileData.findAll('a')
	#print(tableWrapper)

	mapping = []
	for athlete in tableWrapper:
		if 'startlist' in athlete['href']:
			mapping.append(athlete['href'])
	#
	return mapping

def getDataForOneLink(fileData):
	fileData = make_soup(fileData)
	tableWrapper = fileData.findAll('tr', {'data-bind':True})
	
	mapping = []
	for athlete in tableWrapper:
		data = athlete['data-bind'].replace('click: showResult.bind($data, \'athlete\', \'','').replace(')','').split('\', \'')
		mapping.append(data[1])
	#
	#print(mapping)

	return mapping

def main():
	everything = {}
	allLinks = list(set(getAllLinks()))

	allIDs = []
	for link in allLinks:
		fullURL = 'https://www.iaaf.org{}'.format(link)
		data = getURL(fullURL)
		allIDs.extend(getDataForOneLink(data))
		everything.update({link:data})
	
	print(len(allIDs))
	with open('dfdfsdfsdfsdfsf.txt', 'w', encoding='utf-8') as fileS:
		fileS.write(str(allIDs))

	with open('everything.txt', 'w', encoding='utf-8') as fileS1:
		fileS1.write(str(everything))
#

#
main()


