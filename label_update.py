import pywikibot, re, json, mwparserfromhell, collections, sys
from urllib.parse import quote
import toolforge
from datetime import datetime
from customFuncs import basic_sparql as sparql
from customFuncs import get_quarry as quarry
from operator import itemgetter
from natsort import natsorted

conn = toolforge.connect('wikidatawiki_p','analytics')

wiki = pywikibot.Site("wikidata", "wikidata")

SQL = """SELECT page_title,count(*)#concat('{{User:Edgars2007/ID/Template|row|',pl_title,'|',count(*),'}}')
from page
left join pagelinks on pl_title=page_title and pl_from_namespace in (0,146) and pl_namespace=120
where page_namespace=120 and page_is_redirect=0
GROUP BY page_id
ORDER BY count(*) DESC;"""

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query():
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		#cursor.execute('SET connect_timeout=6000;')
		cursor.execute(SQL)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#
def cur_time():
	#2018-04-14T08:59:31
	datetime1 = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
	
	return datetime1
	
current_time = cur_time()



QUERY = """select ?prop ?type ?label_lv ?label_en {
  ?prop wikibase:propertyType ?type .
  optional {?prop rdfs:label ?label_lv filter(lang(?label_lv) = "lv")} .
  optional {?prop rdfs:label ?label_en filter(lang(?label_en) = "en")} .
}"""

def do_sparql():
	res = sparql(QUERY)#eval(open("props-labels-en-lv.json", "r", encoding='utf-8').read())#sparql(QUERY)
	
	disctt = {}
	
	for item in res:
		disctt.update({item['prop']['value'].replace('http://www.wikidata.org/entity/',''):{
							'tips':item['type']['value'].replace('http://wikiba.se/ontology#',''),
							'en':item['label_en']['value'] if 'label_en' in item else '',
							'lv':item['label_lv']['value'].replace('­','') if 'label_lv' in item else ''
		}})
	#
	#pywikibot.output(disctt)
	
	return disctt
#
def do_quarry():
	res = run_query()#res = quarry('16888','1')#eval(open("properties-by-use-count.json", "r", encoding='utf-8').read())#sparql(QUERY)
	
	itemlist = [[encode_if_necessary(item[0]),encode_if_necessary(item[1])] for item in res]
	itemlist.sort(key=lambda k: (-k[1], k[0]))#itemgetter(1), reverse=True)
	#
	#pywikibot.output(itemlist)
	
	timest = 'Update: {{{{ISOdate|{}}}}}'.format(current_time)
	
	
	return itemlist,timest
#
#do_quarry()

######################### lv label page update
def lvlabels(timestamp,quarryres,sparqlres):
	outputtext = timestamp + '. Only the first 1000 results are included.\n\n{|class="sortable wikitable"\n|-\n! Property !! Count of uses !! en label !! Datatype\n|-\n'
	
	counter = 0
	
	for parsingarticle in quarryres:
		article,number = parsingarticle
		
		propptypeSSS = sparqlres[article]#['tips']
		
		#pywikibot.output(propptypeSSS)
		
		lvL = propptypeSSS['lv']
		enL = propptypeSSS['en']
		datatype = propptypeSSS['tips']
			
		if lvL!='':# or datatype=='ExternalId':
			continue
		
		counter +=1
		
		if counter == 1000:
			break
			
		#outputtext = outputtext + "|-\n| {{P|%s}} <small>([[Property talk:%s|talk]])</small> || %d || %s || [https://tools.wmflabs.org/pltools/harvesttemplates/?siteid=en&project=wikipedia&namespace=0&category=&depth=0&property=%s&template=&parameter= Link] || \n" % (article,article,number,propptype,article)
		outputtext = outputtext + "|-\n| {{P|%s}} || %d || %s || %s\n" % (article,number,enL,datatype)
		
		#petscan = quote(petscan)
		
		
	outputtext = outputtext + "|}"
		#pywikibot.output("\t%s-%d - %s" % (article, number, petscan))
		
	#pywikibot.output(outputtext)
	
	
	
	
	report_pageE = pywikibot.Page(wiki,'Wikidata:WikiProject Latvia/Latvian labels')
	report_pageE.text = outputtext
	report_pageE.save(summary='bot: updated', botflag=False, minor=False)
#

def extids(quarryres,sparqlres):
	outputtext = '<pre>\n'
	#outputtext = '{|class="sortable wikitable"\n|-\n! Property !! Count of uses !! en label !! lv label !! Datatype\n|-\n'
	
	#counter = 0
	
	lastupd = 'P1280'
	
	for parsingarticle in quarryres:
	
		article,number = parsingarticle
		
		propptypeSSS = sparqlres[article]#['tips']
		
		#pywikibot.output(propptypeSSS)
		
		lvL = propptypeSSS['lv']
		enL = propptypeSSS['en']
		datatype = propptypeSSS['tips']
			
		if article==lastupd:
			outputtext = outputtext + "=======================\n"
			
		#if lvL!='­' or datatype!='ExternalId':
		#	continue
		#outputtext = outputtext + "|-\n| {{P|%s}} <small>([[Property talk:%s|talk]])</small> || %d || %s || [https://tools.wmflabs.org/pltools/harvesttemplates/?siteid=en&project=wikipedia&namespace=0&category=&depth=0&property=%s&template=&parameter= Link] || \n" % (article,article,number,propptype,article)
		if lvL=='' and datatype=='ExternalId':
			outputtext = outputtext + "%s<tab>%s\n" % (article,enL)
		#outputtext = outputtext + "|-\n| {{P|%s}} || %d || %s || %s || %s\n" % (article,number,enL,lvL,datatype)
		
		#petscan = quote(petscan)
		
		
	outputtext = outputtext + "</pre>"
		#pywikibot.output("\t%s-%d - %s" % (article, number, petscan))
		
	#pywikibot.output(outputtext)
	
	
	#wiki = pywikibot.Site("wikidata", "wikidata")

	report_pageE = pywikibot.Page(wiki,'User:Edgars2007/Latvian-related/ext IDS')
	report_pageE.text = outputtext
	report_pageE.save(summary='bot: updated', botflag=False, minor=False)
#
"""
select * { ?prop wdt:P31 wd:Q19820110 . }
"""
def documentation_props():

	file23doc = sparql('select * { ?prop wdt:P31 wd:Q19820110 . }')#eval(open("props-documentation.json", "r", encoding='utf-8').read())

	discttdoc = [itemdoc['prop']['value'].replace('http://www.wikidata.org/entity/','') for itemdoc in file23doc]
	
	return discttdoc
#
def dormant(timestamp,quarryres,sparqlres):
	discttdoc = documentation_props()
	
	badtemplates = [
						'P368','P369','P578','P1450',
						'P2368','P2535','P2536',
						#īpašību dokumentēšanai: 
						'P1628','P1646','P1647','P2264','P2302'
					]
	
	outputtext = timestamp + '\n\n__TOC__\n== Table ==\n{|class="sortable wikitable"\n|-\n! Property !! Count of uses !! Current count !! Property datatype !! Notes\n|-\n'
	
	quarryres2 = natsorted(quarryres)
	#pywikibot.output(quarryres2)
	
	fsdfsdsdf = []
	
	for parsingarticle in quarryres2:
	
		article,number = parsingarticle
		
		if int(number)>=11:
			continue
		
		propptype = sparqlres[article]['tips']
		
		if article in badtemplates or article in discttdoc:
			#print('skipped:'+article)
			continue
			
		fsdfsdsdf.append(propptype)
		#outputtext = outputtext + "|-\n| {{P|%s}} <small>([[Property talk:%s|talk]])</small> || %d || %s || [https://tools.wmflabs.org/pltools/harvesttemplates/?siteid=en&project=wikipedia&namespace=0&category=&depth=0&property=%s&template=&parameter= Link] || \n" % (article,article,number,propptype,article)
		outputtext = outputtext + "|-\n| {{P|%s}} <small>([[Property talk:%s|talk]])</small> || %d || [https://www.wikidata.org/w/index.php?title=Special:WhatLinksHere&target=Property:%s&namespace=0 Link] || %s || \n" % (article,article,number,article,propptype)
		
		#petscan = quote(petscan)
		
		
	outputtext = outputtext + "|}"
	
	fdfsd = collections.Counter(fsdfsdsdf)
	counterobj = fdfsd.most_common()
	
	rows = []
	
	for letter, count in counterobj:
		rows.append("|-\n| {} || {}".format(letter, count))
		
	outputtext = outputtext + '\n\n== Overview ==\n{|class="sortable wikitable"\n|-\n! Property datatype !! Number of properties in list\n' + '\n'.join(rows) + '\n|}'
	
	
		#pywikibot.output("\t%s-%d - %s" % (article, number, petscan))
		
	#pywikibot.output(outputtext)
	
	
	report_pageE = pywikibot.Page(wiki,'User:Edgars2007/Dormant properties')
	report_pageE.text = outputtext
	report_pageE.save(summary='bot: updated', botflag=False, minor=False)
#
mappingOLD = {
	'Sports properties':['list2'],
	'Association football properties':['list2'],
	'Athletics properties':['list2'],
	'Basketball properties':['list2'],
	'Chess properties':['list2'],
	'Combat sports properties':['list2'],
	'Cycling properties':['list2'],
	'Golf properties':['list2'],
	'Motorsports properties':['list2'],
	'Racket sports properties':['list2'],
	'Rugby properties':['list2'],
	'Water sports properties':['list2'],
	'Winter sports properties':['list2'],
}
mapping123333 = pywikibot.Page(wiki,'User:Edgars2007/Sports IDs/By transclusions/Templates')
mapping = eval(mapping123333.get())


def getparam(tlobject,params):
	for param in params:
	
		if tlobject.has(param):
			opficmlapa = tlobject.get(param).value.strip()
					
			if opficmlapa!='':
			
				return opficmlapa
				break
		
		#else:
	return False

def sports(timestamp,quarryres):
	quary = {d[0]:d[1] for d in quarryres}
	
	
	tplnames_en = ['navbox']
	regex = "{{\s*[Pp]roperty[_ ]talk\s*\|\s*[Pp]?(\d+)\s*}}"
	
	allprops = []
	
	for article in mapping:
		page = pywikibot.Page(wiki,"Template:{}".format(article))
		pagetext = page.get()
		wikicode = mwparserfromhell.parse(pagetext)
		templates = wikicode.filter_templates()
	
		for tpl in templates:
			name = tpl.name.lower().strip().replace('_',' ')
			if name in tplnames_en:
				image_en = getparam(tpl,['list2'])
				if image_en:
					text = image_en
					props = re.findall(regex,text)
					allprops.extend(props)
					break
			
	props = ['P'+d for d in list(set(allprops))]
	
	log2 = open('sport props-list.txt', 'w', encoding='utf-8')
	log2.write(str(props))
	
	resdata = [[d,quary[d]] for d in props if d in quary]
	
	resdata = sorted(resdata, key = lambda x: -int(x[1]))
	
	dfdsfd = ['|-\n| {{{{User:Edgars2007/ID/Template2|{}}}}} || {}'.format(d[0],d[1]) for d in resdata]
	
	tosavedata = timestamp +'\n\n{|class="sortable wikitable"\n|-\n! Property !! Count\n' + '\n'.join(dfdsfd) + '\n|}'
	
	report_pageE = pywikibot.Page(wiki,'User:Edgars2007/Sports IDs/By transclusions')
	report_pageE.text = tosavedata
	report_pageE.save(summary='bot: updated', botflag=False, minor=False)
	

def main():
	sparql_results= do_sparql()
	sql_results,timestamp = do_quarry()
	
	lvlabels(timestamp,sql_results,sparql_results)
	extids(sql_results,sparql_results)
	dormant(timestamp,sql_results,sparql_results)
	sports(timestamp,sql_results)
#
main()