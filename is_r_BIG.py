import requests
import json
import urllib.parse
import pywikibot, re
import toolforge
from datetime import datetime
from customFuncs import basic_sparql as sparql
from customFuncs import get_quarry as quarry

lvsite = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('lvwiki_p')

"""
SELECT * WHERE {
  ?item ^schema:about ?article .
  {?article  wikibase:badge wd:Q17437796} union {?article  wikibase:badge wd:Q17437798} .
  ?item ^schema:about ?articleLV .
  ?articleLV schema:isPartOf <https://lv.wikipedia.org/>
}

SELECT ?item ?articleLV (GROUP_CONCAT(?article; separator=", ") as ?insts) WHERE {
  ?item ^schema:about ?article .
  {?article  wikibase:badge wd:Q17437796} union {?article  wikibase:badge wd:Q17437798} .
  ?item ^schema:about ?articleLV .
  ?articleLV schema:isPartOf <https://lv.wikipedia.org/> .
}
group by ?item ?articleLV
"""

finalquery = """
# get articles
SELECT ?item ?articleLV ?article WHERE {
  ?articleLV schema:about ?item; schema:isPartOf <https://lv.wikipedia.org/> .
  ?item ^schema:about ?article .
  {?article  wikibase:badge wd:Q17437796} union {?article  wikibase:badge wd:Q17437798} .
}
"""

SQL = """select p.page_title, count(l.ll_lang), p.page_len
from langlinks l
join page p on p.page_id=l.ll_from and p.page_namespace=0
group by l.ll_from
having count(l.ll_lang)>99
order by p.page_len asc"""

#lvwiki-20180528sdfsddf-cirrussearch-content.txt
lvdati = open("lvwiki-content-len.txt", "r", encoding='utf-8').read()
lvdati = [f.split('\t') for f in lvdati.split('\n') if len(f)>3]
lvdati = {f[0].replace(' ','_'):f[1] for f in lvdati}


def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query():
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(SQL)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows
#
articlereg = re.compile('(https:\/\/..\.[^\.]+\.org\/wiki\/([^ ]+))')
articlerep = re.compile('(https:\/\/[^\.]+\.[^\.]+\.org\/wiki\/)([^ ]+)')

reg1 = 'https:\/\/([^\.]+)\.wikipedia\.org\/wiki\/'

def list_to_dict(json_data):
	bigm = {}

	for data in json_data:
		lvname = urllib.parse.unquote(data['articleLV']['value'].replace('https://lv.wikipedia.org/wiki/','')).replace(' ','_')
		insts = data['article']['value'] if 'article' in data else ''

		if lvname in bigm:
			bigm[lvname].append(insts)
		else:
			bigm[lvname] = [insts]

	return bigm
#

def addToDict(json_data,currDict):
	blah = currDict
	parsed = list_to_dict(json_data)
	#{"item":{"type":"uri","value":"http://www.wikidata.org/entity/Q1"},"articleLV":{"type":"uri","value":"https://lv.wikipedia.org/wiki/Visums"},"insts":{"type":"literal","value":"https://fi.wikipedia.org/wiki/Maailmankaikkeus, https://nap.wikipedia.org/wiki/Annevierzo, https://scn.wikipedia.org/wiki/Universu, https://ba.wikipedia.org/wiki/%D2%92%D0%B0%D0%BB%D3%99%D0%BC, https://en.wikipedia.org/wiki/Universe, https://nah.wikipedia.org/wiki/Cemanahuac, https://si.wikipedia.org/wiki/%E0%B7%80%E0%B7%92%E0%B7%81%E0%B7%8A%E0%B7%80%E0%B6%BA"}}
	for data in parsed:
		articles = parsed[data]

		goodlangs = []
		for fa in articles:
			languagename = re.search(reg1,fa)
			if languagename:
				extracted = languagename.group(1)

				if len(extracted)==2:
					goodlangs.append(extracted)
		#
		if len(goodlangs)==0:
			continue


		#articles = [urllib.parse.unquote(re.sub(articlerep,r'\2',blah12)) for blah12 in articles if 'wikipedia.org' in blah12]

		#pywikibot.output(item+lvname+plname+coords+insts)
		#pywikibot.output(data)
		#pywikibot.output(articles)
		#if len(articles)==0:
		#	continue
		#print('*'*60)
		#thisdict.update{}
		"""
		if lvname in blah:
				if item not in blah[lvname]:
						#blah[lvname].append([item, coords, insts])
						blah[lvname][0].append(insts)
						#print('here2')
				#else:
				#		print('here')
		else:
				blah[lvname] = [coords, insts]
				#print('here3')
		"""
		blah[data] = articles
	#print('*'*660)
	#pywikibot.output(blah)


	return blah

"""
lvwiki1 = 'quarry-14884-user_treisijs-isakie-raksti-run135974.json'
wikidata1 = 'fa ga wd.json'
lvwiki = json.loads(open(lvwiki1, "r", encoding='utf-8').read())
wikidata = json.loads(open(wikidata1, "r", encoding='utf-8').read())

lvwiki = lvwiki['rows']
wikidata = wikidata['results']['bindings']
"""

lvwiki = run_query()#quarry('14884','1')
wikidata = sparql(finalquery)
#["Keisija_gr\u0113da", "P625", -67.78333333, 62.2]
#lv = {d[0]:[d[1],d[2]] for d in lvwiki}

dsd = {}
wd = addToDict(wikidata,dsd)

rows = []
counter=1

for_list = []
for_out = []

for article in lvwiki:
	#lvdata = lvwiki[article]
	article = [encode_if_necessary(b) for b in article]
	name = article[0].replace(' ','_')
	teksts = lvdati[name] if name in lvdati else 0

	#if name=='NASA': continue

	if name not in wd:
		continue

	if '._gads' in name:
		continue
	wddata = wd[name]
	#row = "|-\n| {}. || [[{}]] || {} || {} || {}".format(counter, name.replace('_',' '), article[2],teksts, len(wddata))
	for_out.append([name.replace('_',' '), article[2],teksts, len(wddata)])
	#counter += 1
	#rows.append(row)
	for_list.append([name, article[2],wddata])
	#counter +=1
	#if counter==150:
	#	break
#
for_out.sort(key=lambda x: int(x[2]))


for article1 in for_out:
	row = "|-\n| {}. || [[{}]] || {} || {} || {}".format(counter, article1[0], article1[1],article1[2], article1[3])
	#for_out.append([name.replace('_',' '), article[2],teksts, len(wddata)])
	counter += 1
	rows.append(row)
"""
while counter<150:

	for article in lvwiki:
		#lvdata = lvwiki[article]
		name = article[0].replace('_',' ')
		if name not in wd:
			continue

		if '. gads' in name:
			continue
		wddata = wd[name]
		row = "|-\n| [[{}]] || {} || {}".format(name, article[2], len(wddata))
		rows.append(row)
		counter +=1
"""

cur_date = datetime.now().strftime("%Y-%m-%d")

table = '\n'.join(rows[:200])
reportpage = """Atjaunināts: {}

{{| class="wikitable sortable"
|-
! Nr.p.k. !! Raksts !! Raksta garums !! Teksta garums !! Vērtīgo/labo rakstu<br>skaits citu valodu<br>Vikipēdijās
{}
|}}
""".format(cur_date,table)

with open("isakieraksti2.txt", "w", encoding='utf-8') as file:
	file.write(str(for_list))

lvpage = pywikibot.Page(lvsite,'Dalībnieks:Edgars2007/Īsākie raksti/Cita versija')
lvpage.text = reportpage

lvpage.save(summary='Bots: atjaunināts', botflag=False, minor=False)
