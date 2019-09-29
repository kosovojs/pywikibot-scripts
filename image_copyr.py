import pywikibot, os, re, requests, sys
from pywikibot.data import api
from datetime import timedelta, datetime
import toolforge

file = open('file_licence.txt','r', encoding='utf-8').read()

site = pywikibot.Site('lv', "wikipedia")
conn = toolforge.connect('lvwiki_p')

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
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
                 from templatelinks
                  WHERE tl_namespace = 10 and tl_from_namespace=6
	and tl_title in ("CC-BY-SA-3.0","Aizsargāts_logo","Self","Copyr","NA-70","Albuma_vāks","PD-nezināms","GreenZeb_attēls","CC-BY-SA-3.0_P","PD-autors","CC-BY-SA-2.5","Panoramio","GFDL","Lidingo11-foto","Ekrānuzņēmums","Filmas_plakāts","Bontrager_foto","CC-BY-SA-4.0","Laurijsfoto","6.2_pants","Grāmatas_vāks","Sedols","PD-likvidēta_prese","Trivial","Edgars2007_attēls","File_other","PD-vecs","Fairuse-audio","R_Vambuts_foto","Driver24-foto","Kikosfoto","MFrikmanis-foto","PD-Demis","Coatofarms","CC-BY-3.0","CC-BY-SA-3.0_PL","Attribution","PD","PD-padomju_prese","Non-free_with_NC","PD-ASV","Strīķis","RAntropovs_foto","Papuass-foto","PD-ASV_valdība","Pastmarka","PD-NASA","PD-Itālija","CC-BY-2.0","CC-BY-2.5","CC-BY-4.0","NOAA","Meteo","CC-BY-SA-2.0","Komikss","LU_fotoarhīvs","PD-zinātne","Rēzekne","PD-Krievija","Ivars_Veiliņš-foto","Gerb","DJ_EV-foto","NMackevičs-foto","GMV-foto","PD-Polija","CC-BY-SA-3.0_P3","CC-BY-SA-3.0_P")
				and tl_from=page_id)
    and img_timestamp>={}	
order by img_timestamp desc"""
#

data = run_query(SQL_main.format(file))
pywikibot.output(data)

if len(data)<1:
	newtimestamp = file
else:
	newtimestamp = encode_if_necessary(data[0][2])

for fil1e in data:
	fil1e = [encode_if_necessary(f) for f in fil1e]
	fileimage = fil1e[0].replace('_',' ')
	page = pywikibot.Page(site,'Attēls:'+fileimage)
	try:
		filetext = page.get(get_redirect=True)
	except pywikibot.exceptions.NoPage:
		continue
	
	if 'ttēla autortiesības' not in filetext:
		filetext = '{{Attēla autortiesības}}\n'+filetext
		page.text = filetext
	
		page.save(comment='{{Attēla autortiesības}}. [[Dalībnieka diskusija:Edgars2007|Kļūda?]]', botflag=False, minor=False)
	
	userpage = pywikibot.Page(site,'Dalībnieka diskusija:'+fil1e[1])
	try:
		userpagetext = userpage.get(get_redirect=True)
	except pywikibot.exceptions.NoPage:
		continue
	
	if fileimage in userpagetext: continue
	
	userpagetext += '\n\n== [[:Attēls:'+fileimage+'|'+fileimage+']] ==\n{{Informācija-autortiesības|'+fileimage+'}}\n--~~~~'
	userpage.text = userpagetext
	
	userpage.save(comment='Bots: nav autortiesību informācijas ([[:Attēls:'+fileimage+']]). [[Dalībnieka diskusija:Edgars2007|Kļūda?]]', botflag=False, minor=False)
#
fileS = open('file_licence.txt','w', encoding='utf-8')
fileS.write(newtimestamp)