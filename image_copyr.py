import pywikibot, os, re, requests, sys
from pywikibot.data import api
from datetime import timedelta, datetime
import toolforge

file = open('file_licence.txt','r', encoding='utf-8').read()

site = pywikibot.Site('lv', "wikipedia")
conn = toolforge.connect('lvwiki_p')
connLabs = toolforge.connect_tools('s53143__meta_p')
cursor1 = connLabs.cursor()

def get_last_run():
	query = "select lastupd from logtable where job='image_copyr'"
	query_res = run_query(query,connLabs)

	return encode_if_necessary(query_res[0][0])
#
def set_last_run(timestamp):
	query = "UPDATE `logtable` SET lastupd=%s where job='image_copyr'"

	timeasUTC = "{0:%Y%m%d%H%M%S}".format(timestamp)
	cursor1.execute(query, (timeasUTC))
	connLabs.commit()
#

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection = conn):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = connection.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows
#
SQL_main = """select img_name, actor_name as img_user_text, img_timestamp
from image
join page on img_name=page_title and page_namespace=6
join actor on img_actor=actor_id
where not exists (select *
                 from templatelinks join linktarget ON tl_target_id = lt_id
                  WHERE lt_namespace = 10 and tl_from_namespace=6
	and lt_title in ("CC-BY-SA-3.0","Aizsargāts_logo","Self","Copyr","NA-70","Albuma_vāks","PD-nezināms","GreenZeb_attēls","CC-BY-SA-3.0_P","PD-autors","CC-BY-SA-2.5","Panoramio","GFDL","Lidingo11-foto","Ekrānuzņēmums","Filmas_plakāts","Bontrager_foto","CC-BY-SA-4.0","Laurijsfoto","6.2_pants","Grāmatas_vāks","Sedols","PD-likvidēta_prese","Trivial","Edgars2007_attēls","File_other","PD-vecs","Fairuse-audio","R_Vambuts_foto","Driver24-foto","Kikosfoto","MFrikmanis-foto","PD-Demis","Coatofarms","CC-BY-3.0","CC-BY-SA-3.0_PL","Attribution","PD","PD-padomju_prese","Non-free_with_NC","PD-ASV","Strīķis","RAntropovs_foto","Papuass-foto","PD-ASV_valdība","Pastmarka","PD-NASA","PD-Itālija","CC-BY-2.0","CC-BY-2.5","CC-BY-4.0","NOAA","Meteo","CC-BY-SA-2.0","Komikss","LU_fotoarhīvs","PD-zinātne","Rēzekne","PD-Krievija","Ivars_Veiliņš-foto","Gerb","DJ_EV-foto","NMackevičs-foto","GMV-foto","PD-Polija","CC-BY-SA-3.0_P3","CC-BY-SA-3.0_P", "PD-self")
				and tl_from=page_id)
    and img_timestamp>={}
order by img_timestamp desc"""
#

lastRun = "{0:%Y%m%d%H%M%S}".format(get_last_run())
data = run_query(SQL_main.format(lastRun))
pywikibot.output(data)

for fil1e in data:
	fil1e = [encode_if_necessary(f) for f in fil1e]
	fileimage = fil1e[0].replace('_',' ')
	page = pywikibot.Page(site,'Attēls:'+fileimage)
	try:
		filetext = page.get(get_redirect=True)
	except pywikibot.exceptions.NoPage:
		continue

	if any([f for f in ['Dzēst','dzēst','Delete','delete'] if "{{"+f in filetext]):
		continue

	if 'ttēla autortiesības' not in filetext:
		filetext = '{{Attēla autortiesības}}\n'+filetext
		page.text = filetext

		page.save(summary='{{Attēla autortiesības}}. [[Dalībnieka diskusija:Edgars2007|Kļūda?]]', botflag=False, minor=False)

	userpage = pywikibot.Page(site,'Dalībnieka diskusija:'+fil1e[1])
	try:
		userpagetext = userpage.get(get_redirect=True)
	except pywikibot.exceptions.NoPage:
		continue

	if fileimage in userpagetext: continue

	userpagetext += '\n\n== [[:Attēls:'+fileimage+'|'+fileimage+']] ==\n{{Informācija-autortiesības|'+fileimage+'}}\n--~~~~'
	userpage.text = userpagetext

	userpage.save(summary='Bots: nav autortiesību informācijas ([[:Attēls:'+fileimage+']]). [[Dalībnieka diskusija:Edgars2007|Kļūda?]]', botflag=False, minor=False)
#
set_last_run(datetime.utcnow())
