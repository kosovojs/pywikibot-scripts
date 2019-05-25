#import MySQLdb as mysqldb
import toolforge
import json
import time
import sys
import codecs
from collections import defaultdict, OrderedDict
from datetime import datetime

begintime = time.time()
print('Begin: {}'.format(begintime))

order = [['enwiki', 34516], ['dewiki', 10103], ['arwiki', 9855], ['frwiki', 8842], ['eswiki', 8296], ['itwiki', 7369], ['plwiki', 6988], ['ptwiki', 6737], ['ruwiki', 6423], ['jawiki', 5430], ['fawiki', 5307], ['nlwiki', 5125], ['zhwiki', 4815], ['svwiki', 4478], ['cawiki', 3976], ['ukwiki', 3833], ['srwiki', 3584], ['fiwiki', 3430], ['hewiki', 3253], ['cswiki', 2991], ['kowiki', 2839], ['shwiki', 2822], ['nowiki', 2558], ['trwiki', 2457], ['idwiki', 2412], ['viwiki', 2322], ['thwiki', 1971], ['simplewiki', 1884], ['huwiki', 1867], ['dawiki', 1864], ['rowiki', 1765], ['slwiki', 1676], ['glwiki', 1644], ['hrwiki', 1574], ['bgwiki', 1527], ['etwiki', 1515], ['euwiki', 1492], ['eowiki', 1433], ['hywiki', 1409], ['hiwiki', 1390], ['elwiki', 1315], ['tawiki', 1300], ['skwiki', 1161], ['cywiki', 1155], ['ltwiki', 1152], ['orwiki', 1143], ['kkwiki', 1127], ['mswiki', 1072], ['gawiki', 1031], ['azbwiki', 1024], ['azwiki', 948], ['bewiki', 924], ['mkwiki', 894], ['mlwiki', 835], ['lvwiki', 819], ['lawiki', 806], ['bswiki', 780], ['nnwiki', 745], ['bnwiki', 732], ['kywiki', 729], ['astwiki', 670], ['urwiki', 670], ['tlwiki', 635], ['uzwiki', 624], ['zh_yuewiki', 619], ['iswiki', 594], ['kawiki', 593], ['tewiki', 576], ['afwiki', 554], ['scowiki', 507], ['iowiki', 481], ['pawiki', 441], ['knwiki', 429], ['be_x_oldwiki', 410], ['sqwiki', 408], ['ckbwiki', 359], ['swwiki', 347], ['zh_min_nanwiki', 325], ['mrwiki', 315], ['dvwiki', 302], ['warwiki', 295], ['siwiki', 295], ['jvwiki', 293], ['ocwiki', 293], ['mywiki', 266], ['ttwiki', 246], ['newiki', 246], ['tgwiki', 227], ['pswiki', 214], ['fywiki', 214], ['lbwiki', 211], ['kuwiki', 207], ['yiwiki', 206], ['iawiki', 200], ['quwiki', 199], ['newwiki', 191], ['brwiki', 191], ['scnwiki', 188], ['suwiki', 178], ['wawiki', 173], ['pnbwiki', 170], ['ndswiki', 159], ['mnwiki', 151], ['wuuwiki', 151], ['alswiki', 149], ['arzwiki', 139], ['htwiki', 135], ['aswiki', 123], ['yowiki', 121], ['guwiki', 119], ['bawiki', 115], ['anwiki', 111], ['emlwiki', 104], ['sawiki', 104], ['liwiki', 103], ['cebwiki', 96], ['lnwiki', 93], ['sowiki', 88], ['sahwiki', 88], ['lmowiki', 84], ['mgwiki', 83], ['bat_smgwiki', 79], ['gdwiki', 79], ['diqwiki', 77], ['gnwiki', 77], ['sdwiki', 77], ['fowiki', 73], ['barwiki', 70], ['jamwiki', 70], ['ruewiki', 67], ['cvwiki', 66], ['xmfwiki', 66], ['amwiki', 65], ['tkwiki', 62], ['cdowiki', 60], ['hakwiki', 59], ['zh_classicalwiki', 58], ['pmswiki', 55], ['zawiki', 54], ['scwiki', 50], ['pamwiki', 47], ['snwiki', 47], ['ilowiki', 46], ['mznwiki', 45], ['bhwiki', 43], ['maiwiki', 43], ['csbwiki', 43], ['bxrwiki', 43], ['bowiki', 42], ['fiu_vrowiki', 40], ['frrwiki', 39], ['lgwiki', 39], ['lijwiki', 37], ['tyvwiki', 35], ['hifwiki', 34], ['aywiki', 34], ['extwiki', 34], ['vecwiki', 33], ['kmwiki', 33], ['kbpwiki', 33], ['rwwiki', 31], ['omwiki', 31], ['piwiki', 30], ['xhwiki', 29], ['bjnwiki', 28], ['ganwiki', 28], ['bclwiki', 27], ['arcwiki', 27], ['sewiki', 27], ['mwlwiki', 26], ['szlwiki', 26], ['nds_nlwiki', 24], ['gvwiki', 24], ['igwiki', 23], ['chrwiki', 22], ['vepwiki', 22], ['dinwiki', 22], ['oswiki', 21], ['roa_rupwiki', 21], ['dtywiki', 21], ['mtwiki', 21], ['nahwiki', 20], ['vlswiki', 20], ['cewiki', 19], ['kshwiki', 19], ['iuwiki', 18], ['lezwiki', 18], ['rnwiki', 18], ['nywiki', 18], ['napwiki', 18], ['tcywiki', 18], ['gomwiki', 18], ['lowiki', 18], ['tiwiki', 17], ['jbowiki', 17], ['furwiki', 17], ['sswiki', 16], ['cowiki', 16], ['ugwiki', 16], ['hawiki', 16], ['akwiki', 16], ['angwiki', 15], ['vowiki', 15], ['kaawiki', 15], ['nsowiki', 15], ['tswiki', 14], ['stwiki', 14], ['minwiki', 13], ['wowiki', 13], ['acewiki', 13], ['papwiki', 12], ['stqwiki', 12], ['novwiki', 11], ['mrjwiki', 11], ['mhrwiki', 11], ['nvwiki', 11], ['lbewiki', 10], ['hsbwiki', 10], ['bmwiki', 10], ['nrmwiki', 10], ['avwiki', 9], ['tnwiki', 9], ['map_bmswiki', 9], ['zeawiki', 9], ['bpywiki', 9], ['iewiki', 8], ['zuwiki', 8], ['kabwiki', 8], ['olowiki', 8], ['myvwiki', 8], ['kiwiki', 8], ['koiwiki', 8], ['kvwiki', 8], ['pcdwiki', 8], ['udmwiki', 7], ['ladwiki', 7], ['lrcwiki', 6], ['ikwiki', 6], ['hawwiki', 6], ['chywiki', 6], ['eewiki', 6], ['mdfwiki', 5], ['xalwiki', 5], ['pdcwiki', 5], ['krcwiki', 5], ['biwiki', 5], ['frpwiki', 5], ['cbk_zamwiki', 4], ['roa_tarawiki', 4], ['kwwiki', 4], ['glkwiki', 4], ['abwiki', 4], ['klwiki', 4], ['srnwiki', 4], ['miwiki', 3], ['pflwiki', 3], ['rmywiki', 3], ['pihwiki', 3], ['kswiki', 3], ['kbdwiki', 3], ['gotwiki', 3], ['vewiki', 2], ['towiki', 2], ['tpiwiki', 2], ['nawiki', 2], ['atjwiki', 2], ['kgwiki', 2], ['pagwiki', 2], ['rmwiki', 2], ['cuwiki', 2], ['smwiki', 1], ['gagwiki', 1], ['tumwiki', 1], ['tetwiki', 1], ['crhwiki', 1], ['dzwiki', 1], ['fjwiki', 1], ['ffwiki', 1], ['chwiki', 1], ['tywiki', 1], ['dsbwiki', 1]][::-1]

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]
#

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

wikis = eval(open('medicine2.txt', 'r', encoding='utf-8').read())

res = {}

filesave = open('medicine4-data-2018.txt', 'a', encoding='utf-8')

for wiki in order:
	counter = 0
	wiki, articles = wiki
	#if wiki in alreadydone: continue
	
	if wiki not in wikis: continue
	
	if wiki=='commonswiki': continue
	
	print(wiki)
	print(str(datetime.now()))
	sys.stdout.flush()
	#conn = mysqldb.connect(wiki.replace('-','_') + ".labsdb", db= wiki.replace('-','_') + '_p',
	#						   read_default_file="~/replica.my.cnf")
	conn = toolforge.connect(wiki.replace('-','_') + '_p')
	for chunk in chunks(wikis[wiki], 100):
		
		chunk = [i.replace("'", "\\'").replace(' ','_') for i in chunk]
		query = "select page_id from page where page_namespace=0 and page_title in ('" + "','".join(chunk) + "');"
		query = query.encode('utf-8')
		#print(query)
		try:
			cursor = conn.cursor()
			cursor.execute(query)
			rows = cursor.fetchall()
		except KeyboardInterrupt:
			sys.exit()
		revids = []
		for row in rows:
			revids.append(str(int(row[0])))
		if not revids:
			counter += 1
			continue
		query = "select rev_user_text, count(*) as count from revision where rev_page in (" + ",".join(revids) + ") and rev_timestamp like '2018%' group by rev_user_text;"
		try:
			cursor = conn.cursor()
			#print('Exec query ' + query)
			#print(counter)
			query = query.encode('utf-8')
			cursor.execute(query)
			rows = cursor.fetchall()
		except KeyboardInterrupt:
			sys.exit()
		thischunksave = []
		for row in rows:
			user = encode_if_necessary(row[0])
			editc = row[1]
			
			thischunksave.append('\t'.join([wiki,str(user),str(editc)]))
		filesave.write('\n'.join(thischunksave)+'\n')
			
		#res_wikis.append(wiki + str(counter))
		#with codecs.open('ffsdfdfsd.json', 'w', 'utf-8') as f:
		#	f.write(str(res))
		#with codecs.open('ffsdfdsfsdfsdfsdfdfsd.json', 'w', 'utf-8') as f:
		#	f.write(json.dumps(res_wikis))
		counter += 1
#
print('done!')
endtime = time.time()
print('End: {}, took so much: {}'.format(endtime,(endtime-begintime)))
sys.stdout.flush()