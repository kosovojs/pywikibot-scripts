import pywikibot, re
import toolforge
from collections import Counter

site = pywikibot.Site('lv', "wikipedia")
conn = toolforge.connect('lvwiki_p')

null = ''

#file = eval(open("quarry-18859-files-without-licence-lvwiki-run179186.json", "r", encoding='utf-8').read())['rows']

SQL = """select img_name, img_user_text, img_timestamp,
	(select GROUP_CONCAT(distinct t1.tl_title separator '|') from templatelinks t1 WHERE t1.tl_from=page_id) as "Used templates",
    (SELECT count(il_from) FROM imagelinks where il_to=img_name) as "Imagelinks"
from image
join page on img_name=page_title and page_namespace=6
where not exists (select *
                 from templatelinks
                  WHERE tl_namespace = 10 and tl_from_namespace=6
	and tl_title in ("CC-BY-SA-3.0","Aizsargāts_logo","Self","Copyr","NA-70","Albuma_vāks","PD-nezināms","GreenZeb_attēls","CC-BY-SA-3.0_P","PD-autors","CC-BY-SA-2.5","Panoramio","GFDL","Lidingo11-foto","Ekrānuzņēmums","Filmas_plakāts","Bontrager_foto","CC-BY-SA-4.0","Laurijsfoto","6.2_pants","Grāmatas_vāks","Sedols","PD-likvidēta_prese","Trivial","Edgars2007_attēls","File_other","PD-vecs","Fairuse-audio","R_Vambuts_foto","Driver24-foto","Kikosfoto","MFrikmanis-foto","PD-Demis","Coatofarms","CC-BY-3.0","CC-BY-SA-3.0_PL","Attribution","PD","PD-padomju_prese","Non-free_with_NC","PD-ASV","Strīķis","RAntropovs_foto","Papuass-foto","PD-ASV_valdība","Pastmarka","PD-NASA","PD-Itālija","CC-BY-2.0","CC-BY-2.5","CC-BY-4.0","NOAA","Meteo","CC-BY-SA-2.0","Komikss","LU_fotoarhīvs","PD-zinātne","Rēzekne","PD-Krievija","Ivars_Veiliņš-foto","Gerb","DJ_EV-foto","NMackevičs-foto","GMV-foto","PD-Polija","CC-BY-SA-3.0_P3","CC-BY-SA-3.0_P","CC-zero")
				and tl_from=page_id)"""

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

file = run_query()

badtpls = ['Imbox','Category_handler','Namespace_detect','Message_box','Arguments','HtmlBuilder','Category_handler','Yesno','Resize','Ambox','Center']

rows = []
users = []
for entry in file:
	entry = [encode_if_necessary(f) for f in entry]
	#["711166115a37875e112c410946a90c4a.jpg", "Maranello Prime", "20160415061150", "Att\u0113la_autorties\u012bbas", 0]
	filename,user,date,tpls,links = entry
	users.append(user)
	date = "{}-{}-{}".format(date[0:4],date[4:6],date[6:8])
	if tpls and tpls!='':
		tpls = tpls.split('|')
		#tpls = ["{{{{tl|{}}}}}".format(f.replace('_',' ')) for f in tpls if '/' not in f]
		tpls = list(set(tpls) - set(badtpls))
		tpls = ["{{{{tl|{}}}}}".format(f.replace('_',' ')) for f in tpls if '/' not in f]
	else:
		tpls = ['']
	
	#todo: ja ir 'Attēla autortiesības', tad rindu iekrāsot sarkanīgu
	row = "|-\n| [[:Attēls:{0}|{0}]] || {{{{U|{1}}}}} || {2} || {3} || {4}".format(filename.replace('_',' '),user,date,', '.join(tpls), links)
	rows.append(row)
	
header = '{{Dalībnieks:Edgars2007/Pieprasīt datu atjaunošanu}}\nSarakstā apkopoti attēli, kam nav norādīta autortiesību licence.\n\n__TOC__\n== Saraksts ==\n{| class="sortable wikitable"\n|-\n! Attēls !! Augšupielādētājs !! Augšupielādes datums !! Izmantotās veidnes !! Saites uz attēlu'
table = '\n'.join(rows)
end = '|}'

finalout = header+'\n'+table+'\n'+end

userstats = Counter(users).most_common()

userstattab = '\n'.join(["|-\n| {{{{User|{0}}}}} || {1}".format(k,v) for k,v in userstats])

usertable = '== Attēli pēc dalībnieka ==\n{| class="sortable wikitable"\n|-\n! Dalībnieks!! Attēli bez licences\n' + userstattab + '\n|}'

finalout = finalout + '\n\n' + usertable + '\n\n[[Kategorija:Vikipēdijas uzlabošanas vikiprojekts — attēli]]'

page = pywikibot.Page(site,'Vikiprojekts:Vikipēdijas uzlabošana/Attēli/Attēli bez licences')
oldtxt = page.get()

page.text = finalout
page.save(comment='Bots: atjaunināts saraksts', botflag=False, minor=False)

#fileS = open("atteli-nav lic.txt", "w", encoding='utf-8')
#fileS.write(finalout)
