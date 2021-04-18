import requests, toolforge

conn = toolforge.connect('wikidatawiki_p','analytics')

allItems = eval(open('dfdfsdfsdfsdfsf.txt', 'r', encoding='utf-8').read())

sparql = """SELECT ?item ?id WHERE {
	?item wdt:P1146 ?id .
}
"""

sqlOO = """SELECT w1.ips_item_id, COUNT(*) as cnt, (select w2.ips_site_page from wb_items_per_site w2 where ips_site_id="lvwiki" and w2.ips_item_id=w1.ips_item_id) as lvwiki
FROM wb_items_per_site w1
where w1.ips_item_id in ({})
group by w1.ips_item_id"""

sqlQ = """SELECT ips_item_id, COUNT(*) as cnt
FROM wb_items_per_site
where ips_item_id in ({})
group by ips_item_id"""

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

def run_query(sqlQuery = '',connectionObj = conn):
	#query = query.encode('utf-8')
	#print(query)
	
	try:
		cursor = connectionObj.cursor()
		cursor.execute(sqlQuery)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#
def getFromSparql():
	data = basic_sparql(sparql)

	toRet = {}
	for one in data:
		toRet.update({
			one["id"]["value"]: one["item"]["value"].replace('http://www.wikidata.org/entity/','')
		})
	
	return toRet
#

def getSitelinks(items):
	finalQ = sqlOO.format(', '.join([f.replace('Q','') for f in items]))
	#print(finalQ)
	results = run_query(finalQ,conn)

	wikipediaList = [[encode_if_necessary(f[0]),encode_if_necessary(f[1]),encode_if_necessary(f[2])] for f in results]

	return wikipediaList
#
def cleanData():
	sparqlData = getFromSparql()
	toRet = []

	for id in sparqlData:
		if id in allItems:
			toRet.append(sparqlData[id])
	
	return toRet

def main():
	finalData = []
	for group in chunker(cleanData(),20):
		data = getSitelinks(group)
		finalData.extend(data)
	
	with open('dfsdsdsdfsdfs.txt', 'w', encoding='utf-8') as fileS:
		fileS.write(str(finalData))
#
main()