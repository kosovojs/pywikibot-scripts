import pymysql, os, json
from itertools import chain
from urllib.parse import urlparse, urlunparse, urlencode

WIKI_LIST = [
	["abwiki", "s3"], ["acewiki", "s3"], ["adywiki", "s3"], ["afwiki", "s3"], ["akwiki", "s3"], ["alswiki", "s3"], ["altwiki", "s5"], ["amwiki", "s3"], ["angwiki", "s3"], ["anwiki", "s3"], ["arcwiki", "s3"], ["arwiki", "s7"], ["arywiki", "s3"], ["arzwiki", "s3"], ["astwiki", "s3"], ["aswiki", "s3"], ["atjwiki", "s3"], ["avkwiki", "s5"], ["avwiki", "s3"], ["awawiki", "s3"], ["aywiki", "s3"], ["azbwiki", "s3"], ["azwiki", "s3"], ["banwiki", "s3"], ["barwiki", "s3"], ["bat_smgwiki", "s3"], ["bawiki", "s3"], ["bclwiki", "s3"], ["bewiki", "s3"], ["be_x_oldwiki", "s3"], ["bgwiki", "s2"], ["bhwiki", "s3"], ["biwiki", "s3"], ["bjnwiki", "s3"], ["bmwiki", "s3"], ["bnwiki", "s3"], ["bowiki", "s3"], ["bpywiki", "s3"], ["brwiki", "s3"], ["bswiki", "s3"], ["bugwiki", "s3"], ["bxrwiki", "s3"], ["cawiki", "s7"], ["cbk_zamwiki", "s3"], ["cdowiki", "s3"], ["cebwiki", "s5"], ["cewiki", "s3"], ["chrwiki", "s3"], ["chwiki", "s3"], ["chywiki", "s3"], ["ckbwiki", "s3"], ["cowiki", "s3"], ["crhwiki", "s3"], ["crwiki", "s3"], ["csbwiki", "s3"], ["cswiki", "s2"], ["cuwiki", "s3"], ["cvwiki", "s3"], ["cywiki", "s3"], ["dagwiki", "s5"], ["dawiki", "s3"], ["dewiki", "s5"], ["dinwiki", "s3"], ["diqwiki", "s3"], ["dsbwiki", "s3"], ["dtywiki", "s3"], ["dvwiki", "s3"], ["dzwiki", "s3"], ["eewiki", "s3"], ["elwiki", "s3"], ["emlwiki", "s3"], ["enwiki", "s1"], ["eowiki", "s2"], ["eswiki", "s7"], ["etwiki", "s3"], ["euwiki", "s3"], ["extwiki", "s3"], ["fawiki", "s7"], ["ffwiki", "s3"], ["fiu_vrowiki", "s3"], ["fiwiki", "s2"], ["fjwiki", "s3"], ["fowiki", "s3"], ["frpwiki", "s3"], ["frrwiki", "s3"], ["frwiki", "s6"], ["furwiki", "s3"], ["fywiki", "s3"], ["gagwiki", "s3"], ["ganwiki", "s3"], ["gawiki", "s3"], ["gcrwiki", "s3"], ["gdwiki", "s3"], ["glkwiki", "s3"], ["glwiki", "s3"], ["gnwiki", "s3"], ["gomwiki", "s3"], ["gorwiki", "s3"], ["gotwiki", "s3"], ["guwiki", "s3"], ["gvwiki", "s3"], ["hakwiki", "s3"], ["hawiki", "s3"], ["hawwiki", "s3"], ["hewiki", "s7"], ["hifwiki", "s3"], ["hiwiki", "s3"], ["hrwiki", "s3"], ["hsbwiki", "s3"], ["htwiki", "s3"], ["huwiki", "s7"], ["hywiki", "s3"], ["hywwiki", "s3"], ["iawiki", "s3"], ["idwiki", "s2"], ["iewiki", "s3"], ["igwiki", "s3"], ["ikwiki", "s3"], ["ilowiki", "s3"], ["inhwiki", "s3"], ["iowiki", "s3"], ["iswiki", "s3"], ["itwiki", "s2"], ["iuwiki", "s3"], ["jamwiki", "s3"], ["jawiki", "s6"], ["jbowiki", "s3"], ["jvwiki", "s3"], ["kaawiki", "s3"], ["kabwiki", "s3"], ["kawiki", "s3"], ["kbdwiki", "s3"], ["kbpwiki", "s3"], ["kgwiki", "s3"], ["kiwiki", "s3"], ["kkwiki", "s3"], ["klwiki", "s3"], ["kmwiki", "s3"], ["knwiki", "s3"], ["koiwiki", "s3"], ["kowiki", "s7"], ["krcwiki", "s3"], ["kshwiki", "s3"], ["kswiki", "s3"], ["kuwiki", "s3"], ["kvwiki", "s3"], ["kwwiki", "s3"], ["kywiki", "s3"], ["ladwiki", "s3"], ["lawiki", "s3"], ["lbewiki", "s3"], ["lbwiki", "s3"], ["lezwiki", "s3"], ["lfnwiki", "s3"], ["lgwiki", "s3"], ["lijwiki", "s3"], ["liwiki", "s3"], ["lldwiki", "s5"], ["lmowiki", "s3"], ["lnwiki", "s3"], ["lowiki", "s3"], ["lrcwiki", "s3"], ["ltgwiki", "s3"], ["ltwiki", "s3"], ["lvwiki", "s3"], ["madwiki", "s5"], ["maiwiki", "s3"], ["map_bmswiki", "s3"], ["mdfwiki", "s3"], ["mgwiki", "s3"], ["mhrwiki", "s3"], ["minwiki", "s3"], ["miwiki", "s3"], ["mkwiki", "s3"], ["mlwiki", "s3"], ["mniwiki", "s5"], ["mnwiki", "s3"], ["mnwwiki", "s3"], ["mrjwiki", "s3"], ["mrwiki", "s3"], ["mswiki", "s3"], ["mtwiki", "s3"], ["mwlwiki", "s3"], ["myvwiki", "s3"], ["mywiki", "s3"], ["mznwiki", "s3"], ["nahwiki", "s3"], ["napwiki", "s3"], ["nawiki", "s3"], ["ndswiki", "s3"], ["nds_nlwiki", "s3"], ["newiki", "s3"], ["newwiki", "s3"], ["niawiki", "s5"], ["nlwiki", "s2"], ["nnwiki", "s3"], ["novwiki", "s3"], ["nowiki", "s2"], ["nqowiki", "s3"], ["nrmwiki", "s3"], ["nsowiki", "s3"], ["nvwiki", "s3"], ["nywiki", "s3"], ["ocwiki", "s3"], ["olowiki", "s3"], ["omwiki", "s3"], ["orwiki", "s3"], ["oswiki", "s3"], ["pagwiki", "s3"], ["pamwiki", "s3"], ["papwiki", "s3"], ["pawiki", "s3"], ["pcdwiki", "s3"], ["pdcwiki", "s3"], ["pflwiki", "s3"], ["pihwiki", "s3"], ["piwiki", "s3"], ["plwiki", "s2"], ["pmswiki", "s3"], ["pnbwiki", "s3"], ["pntwiki", "s3"], ["pswiki", "s3"], ["ptwiki", "s2"], ["quwiki", "s3"], ["rmwiki", "s3"], ["rmywiki", "s3"], ["rnwiki", "s3"], ["roa_rupwiki", "s3"], ["roa_tarawiki", "s3"], ["rowiki", "s7"], ["ruewiki", "s3"], ["ruwiki", "s6"], ["rwwiki", "s3"], ["sahwiki", "s3"], ["satwiki", "s3"], ["sawiki", "s3"], ["scnwiki", "s3"], ["scowiki", "s3"], ["scwiki", "s3"], ["sdwiki", "s3"], ["sewiki", "s3"], ["sgwiki", "s3"], ["shiwiki", "s5"], ["shnwiki", "s3"], ["shwiki", "s5"], ["simplewiki", "s3"], ["siwiki", "s3"], ["skrwiki", "s5"], ["skwiki", "s3"], ["slwiki", "s3"], ["smnwiki", "s5"], ["smwiki", "s3"], ["snwiki", "s3"], ["sowiki", "s3"], ["sqwiki", "s3"], ["srnwiki", "s3"], ["srwiki", "s5"], ["sswiki", "s3"], ["stqwiki", "s3"], ["stwiki", "s3"], ["suwiki", "s3"], ["svwiki", "s2"], ["swwiki", "s3"], ["szlwiki", "s3"], ["szywiki", "s3"], ["tawiki", "s3"], ["taywiki", "s5"], ["tcywiki", "s3"], ["test2wiki", "s3"], ["testwiki", "s3"], ["tetwiki", "s3"], ["tewiki", "s3"], ["tgwiki", "s3"], ["thwiki", "s2"], ["tiwiki", "s3"], ["tkwiki", "s3"], ["tlwiki", "s3"], ["tnwiki", "s3"], ["towiki", "s3"], ["tpiwiki", "s3"], ["trvwiki", "s5"], ["trwiki", "s2"], ["tswiki", "s3"], ["ttwiki", "s3"], ["tumwiki", "s3"], ["twwiki", "s3"], ["tyvwiki", "s3"], ["tywiki", "s3"], ["udmwiki", "s3"], ["ugwiki", "s3"], ["ukwiki", "s7"], ["urwiki", "s3"], ["uzwiki", "s3"], ["vecwiki", "s3"], ["vepwiki", "s3"], ["vewiki", "s3"], ["viwiki", "s7"], ["vlswiki", "s3"], ["vowiki", "s3"], ["warwiki", "s3"], ["wawiki", "s3"], ["wowiki", "s3"], ["wuuwiki", "s3"], ["xalwiki", "s3"], ["xhwiki", "s3"], ["xmfwiki", "s3"], ["yiwiki", "s3"], ["yowiki", "s3"], ["zawiki", "s3"], ["zeawiki", "s3"], ["zhwiki", "s2"], ["zh_classicalwiki", "s3"], ["zh_min_nanwiki", "s3"], ["zh_yuewiki", "s3"], ["zuwiki", "s3"]
]

class Connector:
	db_conn_pool = {}
	mapping = {f[0]:f[1] for f in [*WIKI_LIST, *[['wikidatawiki', 'wikidatawiki']]]}

	def open_connection(self, slice, lang_name):
		kw = {
			'read_default_file': os.path.expanduser("~/replica.my.cnf"),
			'charset': 'utf8mb4',
			'host': '{}.analytics.db.svc.wikimedia.cloud'.format(slice),
			'port': 3306,
			'db': '{}_p'.format(lang_name),
			'cursorclass': pymysql.cursors.SSDictCursor,
			'use_unicode': True,
		}

		mysql = pymysql.connect(**kw)

		mysqlcursor = mysql.cursor()

		return mysql, mysqlcursor

	def get_connection(self, wiki):
		slice = self.mapping.get(wiki)
		if not slice:
			raise Exception('unknown wiki: {}'.format(wiki))

		db_conn_obj = self.db_conn_pool.get(slice)
		if not db_conn_obj:
			db_conn_obj = self.open_connection(slice, wiki)
			self.db_conn_pool.update({slice:db_conn_obj})

		db_conn, db_cursor = db_conn_obj

		db_cursor.execute("use {}_p;".format(wiki))
		db_conn.commit()

		return db_conn_obj

wikis = [f[0] for f in WIKI_LIST]

db_connector = Connector()

wd_conn, wd_cursor = db_connector.get_connection('wikidatawiki')

sql = """SELECT enp.page_title, concat(enel.el_to_domain_index, enel.el_to_path) as el_to
FROM page enp
join externallinks enel on enel.el_from = enp.page_id
WHERE enp.page_namespace = 0 AND enp.page_is_redirect=0 and ({})"""
# having count(enel.el_index)=1

sql_tpl_check = """SELECT ips_site_page
from page
JOIN pagelinks AS wdpl on page_namespace=0 AND page_is_redirect=0 and wdpl.pl_from = page_id
join wb_items_per_site on ips_item_id=substr(page_title,2)*1 and ips_site_id IN (%s)
WHERE wdpl.pl_namespace = 120 AND wdpl.pl_from_namespace = 0 AND wdpl.pl_title = %s"""

def make_sql_query(template_type, url_list):
	mapp = {
		'simple': " ((el_to_domain_index like CONCAT(%s, '%%') or el_to_domain_index like CONCAT(%s, '%%')) and el_to_path like  CONCAT(%s, '%%')) ",
		# 'full': "enel.el_index LIKE CONCAT('%%', %s, '%%')"
	}

	to_join = mapp.get(template_type)

	joined = ' or '.join([to_join] * len(url_list))

	return joined



def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def check_already_has(wiki, prop):
	wd_cursor.execute(sql_tpl_check, (wiki, prop, ))
	resp = wd_cursor.fetchall()
	data = [encode_if_necessary(f['ips_site_page']).replace(' ', '_') for f in resp]

	return data

def flatten_chain(matrix):
	return list(chain.from_iterable(matrix))

def handle_one_wiki(wiki, cursor, prop, urllist, slow_version):
	sql_url_part = make_sql_query('full' if slow_version else 'simple', urllist)
	print(urllist)

	params = [['http://{}'.format(f.get('host')),'https://{}'.format(f.get('host')), f.get('path')] for f in urllist]

	#print([sql.format(sql_url_part), urllist])
	cursor.execute(sql.format(sql_url_part), flatten_chain(params))
	resp = cursor.fetchall()
	data = {encode_if_necessary(f['page_title']): encode_if_necessary(f['el_to']) for f in resp}

	already_has = [] # check_already_has(wiki, prop)

	to_save = set(data) - set(already_has)

	listing = [
		[prop, wiki, f, data[f]]
		for f in to_save
	]

	return listing

res_arr = []

#wikis = ['dewiki']

# ('https://com.national-football-teams', 'http://com.national-football-teams')
# ('transfermarkt',)
# ('https://lv.mantojums', 'http://lv.mantojums')
# ('https://lv.mantojums', 'http://lv.mantojums')#('http://org.olympedia.www./athletes', 'https://org.olympedia.www./athletes')

def transform_url(url):
    if not urlparse(url).scheme:
        url = 'https://' + url

    url_parts = urlparse(url)
    host_parts = url_parts.hostname.split('.')
    new_host = '.'.join(reversed(host_parts))
    transformed_url = new_host + '.'

    new_path = ''
    if url_parts.path:
        new_path += url_parts.path
    if url_parts.query:
        new_path += '?' + url_parts.query

    return {'host': transformed_url, 'path': new_path}


OLD_ = [
	# futbols
	['fifa','P1469',"//com.fifa"],
	['Soccerbase-pl','P2193',"//com.soccerbase.www/players/player"],
	['Soccerbase-man','P2195',"//com.soccerbase.www/managers/manager"],
	['uefa','P2276',"//com.uefa"],
	['soccerway','P2369',"//com.soccerway"],
	['transfermarkt-pl','P2446',"//com.transfermarkt"],
	['transfermarkt-man','P2447',"//com.transfermarkt"],
	['transfermarkt-tiesn','P3699',"//com.transfermarkt"],
	['nft','P2574',"//com.national-football-teams"],
	['scoresway','P3043',"//com.scoresway"],
	['footballdatabase','P3537',"//eu.footballdatabase"],
	['nft','P2574',"//com.national-football-teams"],
	# ziema
	['eliteprosp','P2481',"//com.eliteprospects./player.php"],
	['isufiguresk','P2694',"//com.isuresults.www./bios/"],
	['biatlons','P2459',"//com.biathlonresults.services./athletes.aspx"],
	['speedskatingbase','P2350',"//eu.speedskatingbase.www./"],
	['eurohockey','P2601',"//com.eurohockey.www./player/"],
	['hockeydb','P2602',"//.com.hockeydb.www./"],
	['fil','P2990',"//org.fil-luge.www./"],
	['ibsf','P2991',"//org.ibsf.www./"],#+fibt vecās mājaslapas?
	['worldcurl','P3556',"//com.worldcurl.www./"],
	['worldcurling','P3557',"//org.worldcurling.results./"],
	['hockeyreference','P3598',"//com.hockey-reference.www./players/"],
	['skidb','P3619',"//com.ski-db.www./db/profiles/"],
	['shorttrackonline','P3693',"//info.shorttrackonline.www./"],
	['speedskatingnews','P3694',"//info.speedskatingnews.www./"],
	['schaatsstatistieken','P3695',"//nl.schaatsstatistieken.www./"],
	['speedskatingresults','P4314',"//com.speedskatingresults./"],
	['eliteprospectsStaff','P4319',"//com.eliteprospects.www./staff.php"],

	#['iccf','P3316',"(el_index LIKE 'https://com.iccf.www./player%' or el_index LIKE 'http://com.iccf.www./player%')"],

	#['sportsRef','P1447',"(el_index LIKE 'http://com.sports-reference.www./olympics/athletes/%' or el_index LIKE 'https://com.sports-reference.www./olympics/athletes/%')"],

	#['sportsRef2','P1447',"(el_index LIKE 'http://com.olympicreference.%' or el_index LIKE 'https://com.olympicreference.%')"],
	#['sportsRefOLD','P1447',"el_index LIKE 'http://com.sports-reference.www./olympics/athletes/%'"],
	#['NFT','P2574',"el_index LIKE 'http://com.national-football-teams.www./v2/player.php%'"],##"http://com.national-football-teams.www./v2/player.php%"## "http://com.national-football-teams.www./player/%"
	#['boxrec','P1967',"el_index LIKE 'http://com.boxrec.%'"],
	#['eliteprosp','P2481',"el_index LIKE 'http://com.eliteprospects./player.php?player=%'"],
	#['Cycling Archives','P1409',"el_index LIKE 'http://com.cyclingarchives.www./coureurfiche.php?coureurid=%'"],
	#['judo','P2767',"el_index LIKE 'http://com.judoinside.www./judoka/view/%'"],
	#['isufiguresk','P2694',"el_index LIKE 'http://com.isuresults.www./bios/%'"],
	#['biatlons','P2459',"el_index LIKE 'http://com.biathlonresults.services./athletes.aspx?IbuId=%'"],
	# ['iaaf','P1146',"(el_index LIKE 'http://org.iaaf.www./athletes%' or el_index LIKE 'https://org.iaaf.www./athletes%')"],
	#['chesstempo','P3315',"el_to LIKE 'http://chesstempo.com/gamedb/player/%'"],

    #['imdb','P345',"(el_index LIKE 'http://com.imdb.www./name/nm%' or el_index LIKE 'https://com.imdb.www./name/nm%')"],

    #['fide','P1440',"(el_index LIKE 'http://com.fide.ratings./card.phtml?event=%' or el_index LIKE 'https://com.fide.ratings./card.phtml?event=%')"],

]

to_fetch = [
	#{'prop': 'P2481', 'patterns': ('https://com.eliteprospects', 'http://com.eliteprospects'), 'slow': False},
	#{'prop': 'P2446', 'patterns': ('transfermarkt', ), 'slow': True},
	#{'prop': 'P8286', 'patterns': ('https://org.olympedia', 'http://org.olympedia'), 'slow': False},
	#{'prop': 'P1146', 'patterns': ('https://org.worldathletics', 'http://org.worldathletics'), 'slow': False},
	#{'suffix': 'iaaf', 'prop': 'P1146', 'patterns': ('https://org.iaaf', 'http://org.iaaf'), 'slow': False},
	#{'prop': 'P1440', 'patterns': ('http://com.fide.ratings./card.phtml?event=', 'https://com.fide.ratings./card.phtml?event='), 'slow': False},
	#{'prop': 'P1967', 'patterns': ('http://com.boxrec.', 'https://com.boxrec.'), 'slow': False},
	{'prop': 'P8286', 'patterns': (transform_url('https://olympedia.org/athletes/'), ), 'slow': False},
]

for wiki in wikis:
	print(wiki)
	conn, cursor = db_connector.get_connection(wiki)

	for one in to_fetch:
		PROP = one.get('prop')
		URLS = one.get('patterns')
		slow_version = one.get('slow')
		file_suffix = one.get('suffix', '')

		results = handle_one_wiki(wiki, cursor, PROP, URLS, slow_version)

		if len(results)>0:

			with open('./results2/2024-full-{}-{}{}.json'.format(PROP, wiki, file_suffix), 'w', encoding='utf-8') as file_w:
				file_w.write(json.dumps(results, ensure_ascii=False, indent= 4))
