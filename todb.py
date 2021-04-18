import pywikibot, os, re, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

#os.chdir(r'projects/wpmed')

conn = toolforge.connect('frwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__mis_lists_p')
cursor1 = connLabs.cursor()

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

sql_insert = 'INSERT INTO `entries` (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'

wplist = set(['abwiki', 'acewiki', 'adywiki', 'afwiki', 'akwiki', 'amwiki', 'anwiki', 'angwiki', 'arwiki', 'arcwiki', 'arzwiki', 'aswiki', 'astwiki', 'atjwiki', 'avwiki', 'aywiki', 'azwiki', 'azbwiki', 'bawiki', 'barwiki', 'bclwiki', 'bewiki', 'be_x_oldwiki', 'bgwiki', 'bhwiki', 'biwiki', 'bjnwiki', 'bmwiki', 'bnwiki', 'bowiki', 'bpywiki', 'brwiki', 'bswiki', 'bugwiki', 'bxrwiki', 'cawiki', 'cbk_zamwiki', 'cdowiki', 'cewiki', 'cebwiki', 'chwiki', 'chrwiki', 'chywiki', 'ckbwiki', 'cowiki', 'crwiki', 'crhwiki', 'cswiki', 'csbwiki', 'cuwiki', 'cvwiki', 'cywiki', 'dawiki', 'dewiki', 'dinwiki', 'diqwiki', 'dsbwiki', 'dtywiki', 'dvwiki', 'dzwiki', 'eewiki', 'elwiki', 'emlwiki', 'test2wiki', 'enwiki', 'testwiki', 'simplewiki', 'eowiki', 'eswiki', 'etwiki', 'euwiki', 'extwiki', 'fawiki', 'ffwiki', 'fiwiki', 'fjwiki', 'fowiki', 'frwiki', 'frpwiki', 'frrwiki', 'furwiki', 'fywiki', 'gawiki', 'gagwiki', 'ganwiki', 'gdwiki', 'glwiki', 'glkwiki', 'gnwiki', 'gomwiki', 'gotwiki', 'alswiki', 'guwiki', 'gvwiki', 'hawiki', 'hakwiki', 'hawwiki', 'hewiki', 'hiwiki', 'hifwiki', 'hrwiki', 'hsbwiki', 'htwiki', 'huwiki', 'hywiki', 'iawiki', 'idwiki', 'iewiki', 'igwiki', 'ikwiki', 'ilowiki', 'iowiki', 'iswiki', 'itwiki', 'iuwiki', 'jawiki', 'jamwiki', 'jbowiki', 'jvwiki', 'kawiki', 'kaawiki', 'kabwiki', 'kbdwiki', 'kbpwiki', 'kgwiki', 'kiwiki', 'kkwiki', 'klwiki', 'kmwiki', 'knwiki', 'kowiki', 'koiwiki', 'krcwiki', 'kswiki', 'kshwiki', 'kuwiki', 'kvwiki', 'kwwiki', 'kywiki', 'lawiki', 'ladwiki', 'lbwiki', 'lbewiki', 'lezwiki', 'lgwiki', 'liwiki', 'lijwiki', 'lmowiki', 'lnwiki', 'lowiki', 'lrcwiki', 'ltwiki', 'ltgwiki', 'lvwiki', 'zh_classicalwiki', 'maiwiki', 'map_bmswiki', 'mdfwiki', 'mgwiki', 'mhrwiki', 'miwiki', 'minwiki', 'mkwiki', 'mlwiki', 'mnwiki', 'mrwiki', 'mrjwiki', 'mswiki', 'mtwiki', 'mwlwiki', 'mywiki', 'myvwiki', 'mznwiki', 'nawiki', 'nahwiki', 'zh_min_nanwiki', 'napwiki', 'nowiki', 'ndswiki', 'nds_nlwiki', 'newiki', 'newwiki', 'nlwiki', 'nnwiki', 'novwiki', 'nrmwiki', 'nsowiki', 'nvwiki', 'nywiki', 'ocwiki', 'olowiki', 'omwiki', 'orwiki', 'oswiki', 'pawiki', 'pagwiki', 'pamwiki', 'papwiki', 'pcdwiki', 'pdcwiki', 'pflwiki', 'piwiki', 'pihwiki', 'plwiki', 'pmswiki', 'pnbwiki', 'pntwiki', 'pswiki', 'ptwiki', 'quwiki', 'rmwiki', 'rmywiki', 'rnwiki', 'rowiki', 'roa_tarawiki', 'ruwiki', 'ruewiki', 'roa_rupwiki', 'rwwiki', 'sawiki', 'sahwiki', 'scwiki', 'scnwiki', 'scowiki', 'sdwiki', 'sewiki', 'sgwiki', 'bat_smgwiki', 'shwiki', 'siwiki', 'skwiki', 'slwiki', 'smwiki', 'snwiki', 'sowiki', 'sqwiki', 'srwiki', 'srnwiki', 'sswiki', 'stwiki', 'stqwiki', 'suwiki', 'svwiki', 'swwiki', 'szlwiki', 'tawiki', 'tcywiki', 'tewiki', 'tetwiki', 'tgwiki', 'thwiki', 'tiwiki', 'tkwiki', 'tlwiki', 'tnwiki', 'towiki', 'tpiwiki', 'trwiki', 'tswiki', 'ttwiki', 'tumwiki', 'twwiki', 'tywiki', 'tyvwiki', 'udmwiki', 'ugwiki', 'ukwiki', 'urwiki', 'uzwiki', 'vewiki', 'vecwiki', 'vepwiki', 'viwiki', 'vlswiki', 'vowiki', 'fiu_vrowiki', 'wawiki', 'warwiki', 'wowiki', 'wuuwiki', 'xalwiki', 'xhwiki', 'xmfwiki', 'yiwiki', 'yowiki', 'zh_yuewiki', 'zawiki', 'zeawiki', 'zhwiki', 'zuwiki'])

inp = eval(open('wdapiRES-july.txt', 'r', encoding='utf-8').read())

#'Q1707822': {'nlwiki': 'Syndroom van Pendred', 'enwiki': 'Pendred syndrome', 'cswiki': 'Pendredův syndrom', 'arwiki': 'متلازمة بيندريد', 'frwiki': 'Syndrome de Pendred', 'eswiki': 'Síndrome de Pendred', 'fiwiki': 'Pendredin oireyhtymä', 'ruwiki': 'Синдром Пендреда', 'plwiki': 'Zespół Pendreda', 'dewiki': 'Pendred-Syndrom', 'itwiki': 'Sindrome di Pendred'}

meta = {}

def parse():
	for entry in inp:
		data = inp[entry]
		kopigas = len(set(data) & wplist)
		meta.update({entry:[kopigas,data['enwiki']]})

bigm = {}

for entry in inp:
	data = inp[entry]

	for wiki in wplist:
		if wiki not in data:
			
			if wiki in bigm:
				bigm[wiki].append(entry)
			else:
				bigm[wiki] = [entry]
#
parse()

final = {}

print('starting')
for one in bigm:
	#print(one)
	thiswiki = [[f,meta[f][0],meta[f][1]] for f in bigm[one]]
	thiswiki = sorted(thiswiki, key = lambda x: (-x[1], x[2]))
	#final.update({one:thiswiki[:1500]})
	curr_time = utc_to_local(datetime.utcnow())
	dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
	#print(dateforq1)
	
	#put_db(infobox,result_json,dateforq1)
	cursor1.execute(sql_insert, (one, 'medicine',str(json.dumps(thiswiki)),dateforq1))
	
connLabs.commit()
connLabs.close()
conn.close()
print('Done')
	

#fileS = open('wdapiRES-july-rez.txt', 'w', encoding='utf-8')
#fileS.write(str(final))