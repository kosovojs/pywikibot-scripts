import pywikibot, re, os, collections, sys
from customFuncs import get_quarry as quarry
from natsort import natsorted
import toolforge
from datetime import datetime

#os.chdir(r'projects/treisijs2')

conn = toolforge.connect('wikidatawiki_p','analytics')
lvwiki = pywikibot.Site("lv", "wikipedia")
site = pywikibot.Site("wikidata", "wikidata")
site.login()

IWlimit = 48

SQL = """SELECT ips_item_id, COUNT(ips_item_id), (SELECT GROUP_CONCAT(distinct concat(wb1.ips_site_id, '-frkmarker-',wb1.ips_site_page) separator '|') as 'otherlinks'
										 FROM wb_items_per_site wb1
										 WHERE wb1.ips_site_id in ('enwiki','dewiki','eswiki','ruwiki','frwiki') and wb1.ips_item_id=www.ips_item_id) as 'other links'
FROM wb_items_per_site www
WHERE ips_site_id LIKE '%wiki'
AND NOT ips_site_id='wikidatawiki'
AND NOT ips_site_id='commonswiki'
GROUP BY ips_item_id 
HAVING COUNT(ips_item_id) > 45
AND ips_item_id NOT IN
(SELECT ips_item_id
FROM wb_items_per_site
WHERE ips_site_id='lvwiki')
ORDER BY COUNT(ips_item_id) DESC;"""

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(sqlQuery = SQL,connectionObj = conn):
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
def sql_big_query():
	conn = toolforge.connect('wikidatawiki_p','analytics')
	
	with conn.cursor() as cur:
		cur.execute(SQL)
		rows = cur.fetchall()

		print('Query ended at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		quaryrun1 = []
	
		for one in rows:
			quaryrun1.append([encode_if_necessary(b) for b in one])

		filsess1 = open('treisijs-big-query12121212.txt','w', encoding='utf-8')
		filsess1.write(str(quaryrun1))
	
		return quaryrun1
#
null = ''

def getAllWikis():
	conn_meta = toolforge.connect('meta_p')
	results = run_query("SELECT dbname FROM wiki WHERE family='wikipedia' and is_closed=0",conn_meta)

	wikipediaList = [encode_if_necessary(f[0]) for f in results]

	return set(wikipediaList)

def getAllCurrentWikidataItemsInWikipedia():
	conn_lvwiki = toolforge.connect('lvwiki_p','analytics')

	currWDitemsQuery = run_query("select pp_value from page_props where pp_propname='wikibase_item'",conn_lvwiki)
	currWDitems = [int(encode_if_necessary(b[0])[1:]) for b in currWDitemsQuery]
	currWDitems.append(24575438)#some bug with "Module:Wikidata2" item
	
	return set(currWDitems)

wplist = getAllWikis()#set(['abwiki', 'acewiki', 'adywiki', 'afwiki', 'akwiki', 'amwiki', 'anwiki', 'angwiki', 'arwiki', 'arcwiki', 'arzwiki', 'aswiki', 'astwiki', 'atjwiki', 'avwiki', 'aywiki', 'azwiki', 'azbwiki', 'bawiki', 'barwiki', 'bclwiki', 'bewiki', 'be_x_oldwiki', 'bgwiki', 'bhwiki', 'biwiki', 'bjnwiki', 'bmwiki', 'bnwiki', 'bowiki', 'bpywiki', 'brwiki', 'bswiki', 'bugwiki', 'bxrwiki', 'cawiki', 'cbk_zamwiki', 'cdowiki', 'cewiki', 'cebwiki', 'chwiki', 'chrwiki', 'chywiki', 'ckbwiki', 'cowiki', 'crwiki', 'crhwiki', 'cswiki', 'csbwiki', 'cuwiki', 'cvwiki', 'cywiki', 'dawiki', 'dewiki', 'dinwiki', 'diqwiki', 'dsbwiki', 'dtywiki', 'dvwiki', 'dzwiki', 'eewiki', 'elwiki', 'emlwiki', 'test2wiki', 'enwiki', 'testwiki', 'simplewiki', 'eowiki', 'eswiki', 'etwiki', 'euwiki', 'extwiki', 'fawiki', 'ffwiki', 'fiwiki', 'fjwiki', 'fowiki', 'frwiki', 'frpwiki', 'frrwiki', 'furwiki', 'fywiki', 'gawiki', 'gagwiki', 'ganwiki', 'gdwiki', 'glwiki', 'glkwiki', 'gnwiki', 'gomwiki', 'gotwiki', 'alswiki', 'guwiki', 'gvwiki', 'hawiki', 'hakwiki', 'hawwiki', 'hewiki', 'hiwiki', 'hifwiki', 'hrwiki', 'hsbwiki', 'htwiki', 'huwiki', 'hywiki', 'iawiki', 'idwiki', 'iewiki', 'igwiki', 'ikwiki', 'ilowiki', 'iowiki', 'iswiki', 'itwiki', 'iuwiki', 'jawiki', 'jamwiki', 'jbowiki', 'jvwiki', 'kawiki', 'kaawiki', 'kabwiki', 'kbdwiki', 'kbpwiki', 'kgwiki', 'kiwiki', 'kkwiki', 'klwiki', 'kmwiki', 'knwiki', 'kowiki', 'koiwiki', 'krcwiki', 'kswiki', 'kshwiki', 'kuwiki', 'kvwiki', 'kwwiki', 'kywiki', 'lawiki', 'ladwiki', 'lbwiki', 'lbewiki', 'lezwiki', 'lgwiki', 'liwiki', 'lijwiki', 'lmowiki', 'lnwiki', 'lowiki', 'lrcwiki', 'ltwiki', 'ltgwiki', 'lvwiki', 'zh_classicalwiki', 'maiwiki', 'map_bmswiki', 'mdfwiki', 'mgwiki', 'mhrwiki', 'miwiki', 'minwiki', 'mkwiki', 'mlwiki', 'mnwiki', 'mrwiki', 'mrjwiki', 'mswiki', 'mtwiki', 'mwlwiki', 'mywiki', 'myvwiki', 'mznwiki', 'nawiki', 'nahwiki', 'zh_min_nanwiki', 'napwiki', 'nowiki', 'ndswiki', 'nds_nlwiki', 'newiki', 'newwiki', 'nlwiki', 'nnwiki', 'novwiki', 'nrmwiki', 'nsowiki', 'nvwiki', 'nywiki', 'ocwiki', 'olowiki', 'omwiki', 'orwiki', 'oswiki', 'pawiki', 'pagwiki', 'pamwiki', 'papwiki', 'pcdwiki', 'pdcwiki', 'pflwiki', 'piwiki', 'pihwiki', 'plwiki', 'pmswiki', 'pnbwiki', 'pntwiki', 'pswiki', 'ptwiki', 'quwiki', 'rmwiki', 'rmywiki', 'rnwiki', 'rowiki', 'roa_tarawiki', 'ruwiki', 'ruewiki', 'roa_rupwiki', 'rwwiki', 'sawiki', 'sahwiki', 'scwiki', 'scnwiki', 'scowiki', 'sdwiki', 'sewiki', 'sgwiki', 'bat_smgwiki', 'shwiki', 'siwiki', 'skwiki', 'slwiki', 'smwiki', 'snwiki', 'sowiki', 'sqwiki', 'srwiki', 'srnwiki', 'sswiki', 'stwiki', 'stqwiki', 'suwiki', 'svwiki', 'swwiki', 'szlwiki', 'tawiki', 'tcywiki', 'tewiki', 'tetwiki', 'tgwiki', 'thwiki', 'tiwiki', 'tkwiki', 'tlwiki', 'tnwiki', 'towiki', 'tpiwiki', 'trwiki', 'tswiki', 'ttwiki', 'tumwiki', 'twwiki', 'tywiki', 'tyvwiki', 'udmwiki', 'ugwiki', 'ukwiki', 'urwiki', 'uzwiki', 'vewiki', 'vecwiki', 'vepwiki', 'viwiki', 'vlswiki', 'vowiki', 'fiu_vrowiki', 'wawiki', 'warwiki', 'wowiki', 'wuuwiki', 'xalwiki', 'xhwiki', 'xmfwiki', 'yiwiki', 'yowiki', 'zh_yuewiki', 'zawiki', 'zeawiki', 'zhwiki', 'zuwiki'])

def titles1(titles):
	for title in titles:
		if title=='':
			#pirmo_kartu_izturejis.append(entry)
			return True
		try:
			secpart = title.split('-frkmarker-')[1]
		except IndexError:
			#pywikibot.output(title)
			return False
		if secpart.startswith(('Category:','Categoría:','Категория:','Kategorie:','Catégorie:','Vorlage:','Plantilla:','Шаблон:','Template:','Wikipedia:','Википедия:','Portal:','Hilfe:','Help:','Mediawiki:','MediaWiki:','Module:')):
			return False
			
		if title.startswith('enwiki-') and re.search('^(AD )?\d+(s|s \(decade\))?( BC)?$',secpart):
			return False
	
	return True


def pirma_apstrade(sqlinputdata):
	null = ''
	file = sqlinputdata#quarry('19261','1')

	allWDITEmsInWIki = getAllCurrentWikidataItemsInWikipedia()

	pirmo_kartu_izturejis = []
	for entry in file:
		#[30089, 117, "eswiki-frkmarker-625|ruwiki-frkmarker-625 \u0433\u043e\u0434|dewiki-frkmarker-625|enwiki-frkmarker-625"]
		wdid,iws,titles = entry

		if wdid in allWDITEmsInWIki: continue

		try:
			titles = titles.split('|')
		except AttributeError:
			titles = []
		#ewiki-frkmarker-Unicode|eswiki-frkmarker-Unicode|ruwiki-frkmarker-Unicode|enwiki-frkmarker-Unicode
		#Autorenportal|ruwiki-frkmarker-Портал сообщества|eswiki-frkmarker-Comunidad|enwiki-frkmarker-Wikipedia:Community portal
		#ruwiki-frkmarker-Википедия:Представление системе|dewiki-frkmarker-Anmelden|enwiki-frkmarker-Logging in|eswiki-frkmarker-Ayuda:Registro
		titlecheck = titles1(titles)
		
		if int(iws)<IWlimit: continue
		
		if titlecheck:
			pirmo_kartu_izturejis.append(entry)
			
	otro_kartu = {}
	for row in pirmo_kartu_izturejis:
		wdid,iws,titles = row
		try:
			entitles = {f.split('-frkmarker-')[0]:f.split('-frkmarker-')[1] for f in titles.split('|') if len(f)>3}
			entitle = entitles['enwiki'] if 'enwiki' in entitles else ''
			rutitle = entitles['ruwiki'] if 'ruwiki' in entitles else ''
		except AttributeError:
			entitle = ''
			rutitle = ''
		otro_kartu.update({'Q'+str(wdid):[iws,entitle,rutitle]})
	#
	#print(len(otro_kartu))
	#pywikibot.output(otro_kartu[:150])

	#cur_items = get_current_list()
	#otrakarta2 = ['Q'+str(f[0]) for f in otro_kartu]

	salidz = list(set(otro_kartu))#list(set(otro_kartu) - set(cur_items))
	print(len(salidz))

	filsess1 = open('quarry-19261-fsfsuntitled-run182282.txt','w', encoding='utf-8')
	filsess1.write(str(salidz))
	
	return salidz
#
def doAPI(wditems):
	r = ''
	idlist = '|'.join(wditems)
	r = pywikibot.data.api.Request(site=site, action="wbgetentities", 
									props="sitelinks|descriptions|claims", ids=idlist,redirects='yes').submit()
									
	#pywikibot.output(r)
	return r
	

def processone(entity):
	#data = filedata[entity]
	#pywikibot.output(data['sitelinks'])
	sitelinks = entity['sitelinks']
	#varbūt pēc tam sakārtot alfabētiskā secībā, ja ir saraksts, nevis dict
	newlinks = {wiki:sitelinks[wiki]['title'] for wiki in sitelinks}# if re.match(regexiw,wiki) or wiki in otherwikis]
	
	claims = entity["claims"]
	if 'P31' not in claims:
		p31vals = []
	else:
		p31vals = [f["mainsnak"]["datavalue"]["value"]["id"] for f in claims['P31']]
	if 'P279' not in claims:
		pP279vals = []
	else:
		pP279vals = [f["mainsnak"]["datavalue"]["value"]["id"] for f in claims['P279']]
		#masivcs.update({entry:p31vals})
	
	#pywikibot.output(newlinks)
	descmas = entity['descriptions']
	desc = {val:descmas[val]['value'] for val in descmas}
	
	return [newlinks,pP279vals,p31vals,desc]
	
	#p31claims = data['claims']
#

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#
def api_wrap(inputdata):
	filedataREZ = open('tresija saraksts_raw201704-123.txt','w', encoding='utf-8')
	object = {}

	groupfd=0
	for group in chunker(inputdata,50):
		print(groupfd)
		groupfd += 1
		entis = doAPI(group)['entities']
		entitylist = entis.keys()
		
		for entdata in entitylist:
			object.update({entdata:processone(entis[entdata])})
			
	#pywikibot.output(object)
	#filedataREZ.write(str(object))                                    - SALABOT - ir memory error
	
	return object
#
def tresa_dala(inputd):
	p31Andp279 = []
	object = []
	for entry in inputd:
		#[newlinks,pP279vals,p31vals,desc]
		entdata = inputd[entry]
		
		thisdesc = ''
		thislink = ''
		newlinks,pP279vals,p31vals,desc = entdata
		
		#newlinks2 = [wiki for wiki in newlinks if re.match(regexiw,wiki) or wiki in otherwikis]
		iwcount = len(set(newlinks)&wplist)
		if iwcount<IWlimit:
			continue
		gfdgf = False
		badvals = ['Q11266439','Q4167836','Q4167410']
		for badv in badvals:
			if badv in p31vals:
				gfdgf = True
				break
		#
		if gfdgf:
			continue
		
		p31Andp279.extend(pP279vals)
		p31Andp279.extend(p31vals)
		
		#desc
		descfallback = ['en','ru','de']
		for langD in descfallback:
			if langD in desc:
				thisdesc = desc[langD]
				break
				
		for langS in descfallback:
			if langS+'wiki' in newlinks:
				thislink = [langS,newlinks[langS+'wiki']]
				break
		#
		object.append([entry,thisdesc,thislink,p31vals,pP279vals,iwcount])
	
	return object
#
header = """{| class='sortable wikitable'
|-
! Vikidati !! Wiki !! Apraksts !! IW
"""

def final_func(fileO):
	fileO.sort(key=lambda x: -int(x[5]))

	object = []

	for entry in fileO:
		
		entry1,thisdesc,thislink,p31vals,pP279vals,iwcount = entry
		
		#iwcount = len(set(wikis)&wplist)
		
		if thisdesc!='':
			whattoputindesc = thisdesc
		#elif len(p31vals)>0:
		#	whattoputindesc = p31vals
		#elif len(pP279vals)>0:
		#	whattoputindesc = pP279vals
		else:
			whattoputindesc = ''
		#
		if len(thislink)>0:
			
			formatwikilink = "[[:{0}:{1}|{1}]] <small>({0})</small>".format(thislink[0],thislink[1])
		else:
			formatwikilink = ''
		thisrow = "|-\n| [[:d:{0}]] || {1} || {2} || {3}".format(entry1,formatwikilink,whattoputindesc,iwcount)
		object.append(thisrow)
	#
	toret = header + '\n'.join(object) + '\n|}'

	#print(len(object))
	fileS1 = open('tresija sarfdfsaksts_raw201704-gatavs24234.txt','w', encoding='utf-8')
	#fileS12 = open('tresija saraksts_raw201704-insts.txt','w', encoding='utf-8')
	fileS1.write(str(toret))
	#fileS12.write(str(collections.Counter(p31Andp279).most_common()))
	
	return toret
#

intro = '''{{Dalībnieks:Edgars2007/Pieprasīt datu atjaunināšanu}}
Šajā uzskaitījumā ir tie gadu raksti, kas nav latviešu valodas Vikipēdijā, bet ir 51 un vairāk citu valodu Vikipēdijās.

Datums: ~~~~~.

__TOC__
'''

header1 = '''{| class="sortable wikitable"
|-
! width="320" | Vajadzīgais raksts
! width="320" | Saite uz Vikidatiem (nosaukums angļu valodā)
! "Starpviki"<br />skaits
! data-sort-type="isoDate"| Pēdējo reizi atjaunots<br />(gads-mēn.-dat.)
|-
'''

def year_page(sqlinputdata):
	null = ''
	file = sqlinputdata#quarry('19261','1')
	cur_date = datetime.now().strftime("%Y-%m-%d")
	bigmas = {}

	converter = {
		'\d+':'me-g',
		'\d+(s|s \(decade\))':'me-d',
		'\d+ BC':'pme-g',
		'\d+s BC(\(decade\))?':'pme-d'
	}

	def titles1(titles,wdid,iws):
		for title in titles:
			try:
				secpart = title.split('-frkmarker-')[1]
			except IndexError:
				#pywikibot.output(title)
				return False
			
			if not title.startswith('enwiki-'): continue
			
			if not re.search('^(AD )?\d+(s|s \(decade\))?( BC)?$',secpart): continue
			
			for tips in converter:
				if re.search('^{}$'.format(tips),secpart):
					thistype = converter[tips]
					
					if thistype in bigmas:
						bigmas[thistype].append([secpart,wdid,iws])
					else:
						bigmas[thistype] = [[secpart,wdid,iws]]
	#
	pirmo_kartu_izturejis = []
	for entry in file:
		#[30089, 117, "eswiki-frkmarker-625|ruwiki-frkmarker-625 \u0433\u043e\u0434|dewiki-frkmarker-625|enwiki-frkmarker-625"]
		wdid,iws,titles = entry
		try:
			titles = titles.split('|')
		except AttributeError:
			titles = []
		#ewiki-frkmarker-Unicode|eswiki-frkmarker-Unicode|ruwiki-frkmarker-Unicode|enwiki-frkmarker-Unicode
		#Autorenportal|ruwiki-frkmarker-Портал сообщества|eswiki-frkmarker-Comunidad|enwiki-frkmarker-Wikipedia:Community portal
		#ruwiki-frkmarker-Википедия:Представление системе|dewiki-frkmarker-Anmelden|enwiki-frkmarker-Logging in|eswiki-frkmarker-Ayuda:Registro
		if int(iws)<52: continue
		
		titlecheck = titles1(titles,wdid,iws)
	#
	filsess1 = open('treisijs-gadi-51.txt','w', encoding='utf-8')
	filsess1.write(str(bigmas))

	structure = {
		'sec':['me','pme'],
		'names':{'me':'Mūsu ēra','pme':'Pirms mūsu ēras'},
	}

	def make_lv(en,lv,patt):
		return re.sub(patt,lv,en)

	def make_table(data,tips):
		sec = natsorted(data,key = lambda x: (-x[2],x[0]))
		#['1450s', 83023, 77]
		
		tableo = ['| [[{}]]||[[:d:Q{}|{}]]||{}||{}\n'.format(make_lv(f[0],tips[0],tips[1]),
															f[1],
															f[0],
															f[2],
															cur_date
															) for f in sec]
		#
		return header1 + '|-\n'.join(tableo) + '|}'
	#

	def make_wp():
		sdasd = []
		meG = bigmas['me-g'] if 'me-g' in bigmas else []
		meD = bigmas['me-d'] if 'me-d' in bigmas else []
		pmeG = bigmas['pme-g'] if 'pme-g' in bigmas else []
		pmeD = bigmas['pme-d'] if 'pme-d' in bigmas else []
		
		if (len(meG)>0 or len(meD)>0):
			sdasd.append('\n== Mūsu ēra ==')
			
			if len(meG)>0:
				sdasd.append('\n=== Gadi ===')
				sdasd.append(make_table(meG,(r'\1. gads','^(\d+)')))
			
			if len(meD)>0:
				sdasd.append('\n=== Desmitgades ===')
				sdasd.append(make_table(meD,(r'\1. gadi','^(\d+)(s(.*)?)')))
		
		if (len(pmeG)>0 or len(pmeD)>0):
			sdasd.append('\n== Pirms mūsu ēras ==')
			
			if len(pmeG)>0:
				sdasd.append('\n=== Gadi ===')
				sdasd.append(make_table(pmeG,(r'\1. gads p.m.ē.','^(\d+)(.*)?')))
			
			if len(pmeD)>0:
				sdasd.append('\n=== Desmitgades ===')
				sdasd.append(make_table(pmeD,(r'\1. gadi p.m.ē.','^(\d+)(s(.*)?)')))
		
		return '\n'.join(sdasd)
	#

	tosave = intro + make_wp() + '\n\n[[Kategorija:Vikipēdija]]'

	filsessfsd1 = open('treisijs-gadi-51-v2.txt','w', encoding='utf-8')
	filsessfsd1.write(str(tosave))
	
	save_wiki('Vikipēdija:Raksti, kas nav latviešu valodas Vikipēdijā, bet ir visvairāk citu valodu Vikipēdijās/Gadi',tosave)
#

def dataSaving(data):
	conn = toolforge.connect_tools('s53143__missing_p')
	cursor = conn.cursor()
	
	cursor.execute("TRUNCATE TABLE articles")
	conn.commit()
	
	sql = "INSERT INTO articles (wd, orig, lang, descr, wiki, iws) VALUES (%s, %s, %s, %s, %s, %s)"
	
	for one in data:
		wd, orig, lang, descr,  iws = one
		cursor.execute(sql, (wd, orig, lang, descr, 'lvwiki', iws))
	#
	conn.commit()
	
	dateforq12 = "{0:%Y-%m-%d}".format(datetime.utcnow())
	sql2 = 'UPDATE meta set value= %s where data="upd" and wiki="lvwiki"'
	cursor.execute(sql2, (dateforq12))
	conn.commit()
	
	conn.close()
#
def saveDataToDB(savingData):
	blah = []
	#lvdata = eval(open('lvMAP.json','r', encoding='utf-8').read())
	itemdata = savingData#eval(open('treisijs-gadi-51-v2sdfsdfsdfsdfsfsdfd.txt','r', encoding='utf-8').read())
	for item in itemdata:
		if item[1]!='Wikimedia template':
			#['Q204249', 'city in Japan, seat of Ibaraki Prefecture', ['en', 'Mito, Ibaraki'], ['Q1145012', 'Q17221353'], [], 52]
			try:
				blah.append([item[0][1:], item[2][1], item[2][0], item[1], item[5]])
			except:
				pywikibot.output(item)
	blah.sort(key=lambda x: -int(x[4]))
	
	return blah
	
	fileforsave = open('db-save-dec.txt','w', encoding='utf-8')
	fileforsave.write('\n'.join(['\t'.join(map(str,f)) for f in blah]))
	
	
#

def save_wiki(article,text):
	lvpage = pywikibot.Page(lvwiki,article)
	lvpage.text = text
	
	lvpage.save(summary='Bots: atjaunināts', botflag=False, minor=False)

def main():
	print('Started at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	
	
	sqlinputdata = sql_big_query()#eval(open('treisijs-big-query12121212.txt','r', encoding='utf-8').read())#sql_big_query()
	wditemsforapi = pirma_apstrade(sqlinputdata)
	
	#wditemsforapi = eval(open('quarry-19261-fsfsuntitled-run182282.txt','r', encoding='utf-8').read())
	apires = api_wrap(wditemsforapi)
	
	#apires = eval(open('tresija saraksts_raw201704-123.txt','r', encoding='utf-8').read())
	beforefinall = tresa_dala(apires)
	
	#filsessfsd1 = open('treisijs-gadi-51-v2sdfsdfsdfsdfsfsdfd.txt','w', encoding='utf-8')
	#filsessfsd1.write(str(beforefinall))
	
	#beforefinall = eval(open('treisijs-gadi-51-v2sdfsdfsdfsdfsfsdfd.txt','r', encoding='utf-8').read())#sql_big_query()
	dataSaving(saveDataToDB(beforefinall))
	#important = final_func(beforefinall)
	#save_wiki('Dalībnieks:Edgars2007/51++',important)
	
	year_page(sqlinputdata)
#
#
main()
