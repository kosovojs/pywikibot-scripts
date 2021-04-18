import requests, toolforge

#null = None

allIDs = eval(open('dfdfsdfsdfsdfsf.txt', 'r', encoding='utf-8').read())
allSitelinks = eval(open('dfsdsdsdfsdfs.txt', 'r', encoding='utf-8').read())

sparql = """SELECT ?item ?id WHERE {
	?item wdt:P1146 ?id .
}
"""

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#
def basic_sparql(query):
	
	payload = {
		'query': query,
		'format': 'json'
	}

	r = requests.get('https://query.wikidata.org/bigdata/namespace/wdq/sparql?', params=payload)
	r.encoding = 'utf-8'
	json_data = eval(r.text)
	
	#items = [f["item"]["value"].replace('http://www.wikidata.org/entity/','') for f in json_data['results']['bindings']]
	
	return json_data['results']['bindings']

def getFromSparql():
	data = basic_sparql(sparql)

	toRet = {}
	for one in data:
		toRet.update({
			one["id"]["value"]: one["item"]["value"].replace('http://www.wikidata.org/entity/','')
		})
	
	return toRet
#

def cleanData():
	
	toRet = []

	for row in allSitelinks:
		#[468204, 11, None]
		wd, iws, lv = row
		if lv: continue

		toRet.append([wd,iws])
	
	return toRet

def main():
	sparqlData = getFromSparql()
	sitelinks = cleanData()

	sitelinks.sort(key = lambda x: -x[1])
	
	final = ["* {{{{Q|{}}}}} - {}".format(f[0],f[1]) for f in sitelinks]

	with open('dsfsdfsdfsdfsdfsdfsdfsdfsdfsdfsd.txt', 'w', encoding='utf-8') as fileS:
		fileS.write('{{div col|4}}\n'+'\n'.join(final[:150])+'\n{{div col end}}')
#
main()