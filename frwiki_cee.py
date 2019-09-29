import pywikibot
import toolforge
import re
import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

conn = toolforge.connect('frwiki_p','analytics')

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

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

def format_frwiki(infoboxname,data):
	
	ret = []
	for row in data:
		if infoboxname=='indija':
			langs,fr,en,wd,infobox = row
			
			if not infobox:
				infobox = ''
			infs = infobox.split('|')
			
			if 'Infobox_Subdivision_administrative' in infs: continue
			if 'Infobox_Biographie2' in infs: continue
			if 'Infobox_Politicien' in infs: continue
			
			
		else:
			langs,fr,en,wd = row
			
		if en!='':
			ret.append([en,langs,wd])
		else:
			pywikibot.output(row)
	return ret
#
def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

#infoboxlist = infoboxlist[::-1]

#sql_insert = 'UPDATE `entries` INTO (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'
sql_update = 'UPDATE `entries` SET jsondata=%s, last_upd=%s where group_name=%s and name=%s'


jsoninput = [
	{'group':'other','name':'Irāna','frwiki':'Iran'},
	{'group':'other','name':'Irāka','frwiki':'Irak'},
]

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def get_page_info_chunk(SQL,pages):
	query_res = run_query(SQL.format(', '.join(map(str,pages))))
	query_res = [encode_all_items(f) for f in query_res]
	
	#query_res = {f[0]:f[1:] for f in query_res}
	
	return query_res
#
def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#
def checkTitle(project, page_data):
	project = project.lower().replace(' ','_')
	title = page_data[1].replace('_',' ')
	
	
	if project == "monde_antique":
		if re.search('^(AD )?\d+s?(\sBC)?',title):
			return False
	elif project == "monde_indien":
		infoboxes = page_data[3].replace('_',' ')
		if not infoboxes:
			infoboxes = ""
		
		infs = infoboxes.split('|')
		
		if 'Infobox_Subdivision_administrative' in infs: return False
		if 'Infobox_Biographie2' in infs: return False
		if 'Infobox_Politicien' in infs: return False
	elif project == "japon":
		infoboxes = page_data[3].replace('_',' ')
		if not infoboxes:
			infoboxes = ""
		
		infs = infoboxes.split('|')
		
		if 'Infobox Localité' in infs: return False
		#if 'Infobox_Biographie2' in infs: return False
		#if 'Infobox_Politicien' in infs: return False
	
	return True
	
def merge_res(iw_mas,info,project):
	final = []
	errors = []
	
	for page_id in iw_mas:
		if page_id not in info:
			errors.append([page_id,iws])
			continue
		
		iws = iw_mas[page_id]
		
		page_info = info[page_id]
		
		if page_info[1]==None:#no enwiki title
			continue
		
		isValidTitle = True
		
		if project in ['Monde antique']:
			isValidTitle = checkTitle(project,page_info)
		
		if isValidTitle:
			curr_item = [page_info[1],iws,page_info[2]]
			final.append(curr_item)
	#
	a = sorted(final, key=lambda x: -int(x[1]))
	
	return [a,errors]
#
def get_page_info(pages):
	alldata = []
	
	SQL = """select page_id, page_title,
	(select m2.ll_title from langlinks m2 where m2.ll_from=p.page_id and m2.ll_lang="en")  as en,
	(select pp.pp_value from page_props pp where pp.pp_page=p.page_id and pp_propname='wikibase_item') as wd,
	(SELECT GROUP_CONCAT(tl_title SEPARATOR '|') FROM templatelinks            WHERE tl_title like 'Infobox%' and tl_namespace = 10 and tl_from=p.page_id) as box
	from page p
	where p.page_namespace=0 and p.page_is_redirect=0 and p.page_id in ({})"""
	
	for chunk in chunker(pages, 50):
		thispart = get_page_info_chunk(SQL,chunk)
		alldata.extend(thispart)
	#
	return alldata
#
def one_project(project):
	number = "2500"# if project=="Monde antique" else "1000"
	
	SQL = """select count(l.ll_lang) as langs, ll_from
		from langlinks l
		where not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
			and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
															and cla.cl_to="{}"
					   )
		group by l.ll_from
		order by count(l.ll_lang) desc
	limit {};""".format(project.replace(' ','_'),number)
	
	query_res = run_query(SQL)
	query_res = [[encode_if_necessary(f[0]),encode_if_necessary(f[1]),project] for f in query_res]
	
	return query_res
#
infoboxes = ["Portail:Albanie/Articles_liés",
"Portail:Arménie/Articles_liés",
"Portail:Autriche/Articles_liés","Portail:Innsbruck/Articles_liés","Portail:Vienne_(Autriche)/Articles_liés",
"Portail:Empire_autrichien/Articles_liés",
"Portail:Azerbaïdjan/Articles_liés",
"Portail:Bakou/Articles_liés",
"Portail:Biélorussie/Articles_liés",
#Bashkortostan- nav
#krimas tatāri
#don region
#erzji
"Portail:Bosnie-Herzégovine/Articles_liés",
"Portail:Bulgarie/Articles_liés",
"Portail:République_tchèque/Articles_liés",#vrb atsevišķi
"Portail:Tchécoslovaquie/Articles_liés","Portail:Prague/Articles_liés",
#esperanto
"Portail:Géorgie_(pays)/Articles_liés",
#grieķija
"Portail:Croatie/Articles_liés",
#igaunija, krievija, lietuva
"Portail:Macédoine/Articles_liés","Portail:Skopje/Articles_liés",
"Portail:Moldavie/Articles_liés",
#polija
#sorbi
#tatarstana
"Portail:Roumanie/Articles_liés","Portail:Bucarest/Articles_liés",
#Republika Srpska
"Portail:Serbie/Articles_liés","Portail:Belgrade/Articles_liés",
"Portail:Slovaquie/Articles_liés","Portail:Bratislava/Articles_liés","Portail:Košice/Articles_liés",
#ukraina
"Portail:Hongrie/Articles_liés","Portail:Budapest/Articles_liés",
                   #########
"Portail:Grèce/Articles_liés","Portail:Athènes/Articles_liés","Portail:Crète/Articles_liés","Portail:Grèce_antique/Articles_liés",
"Portail:Kazakhstan/Articles_liés",
"Portail:Chypre/Articles_liés",
"Portail:Kosovo/Articles_liés",
"Portail:Monténégro/Articles_liés",
"Portail:Slovénie/Articles_liés",
"Portail:Turquie/Articles_liés","Portail:Istanbul/Articles_liés","Portail:Empire_ottoman/Articles_liés",
    
    "Portail:Estonie/Articles_liés","Portail:Tallinn/Articles_liés",
"Portail:Lituanie/Articles_liés",
"Portail:Pologne/Articles_liés","Portail:Varsovie/Articles_liés","Portail:Cracovie/Articles_liés",
"Portail:Ukraine/Articles_liés",
"Portail:Russie/Articles_liés","Portail:Sibérie/Articles_liés","Portail:Moscou/Articles_liés",
"Portail:Oblast_de_Novossibirsk/Articles_liés","Portail:Saint-Pétersbourg/Articles_liés","Portail:Sotchi/Articles_liés",
"Portail:Empire_russe/Articles_liés","Portail:URSS/Articles_liés"]

def main():
	allarticles = []
	for infobox in infoboxes:
		#fr = infobox['frwiki']
		pywikibot.output('\t'+infobox)
			
		result_json = one_project(infobox)
		allarticles.extend(result_json)
	#
	with open("cee-allarticles.txt", "w", encoding='utf-8') as fileSave:
		fileSave.write(str(allarticles))
	#
	allarticles = list(set([f[1] for f in allarticles]))
	pageinfo = get_page_info(allarticles)

	with open("cee-allarticle-data.txt", "w", encoding='utf-8') as fileSave:
		fileSave.write(str(pageinfo))
		
	#conn.close()
	pywikibot.output('done')
#
main()