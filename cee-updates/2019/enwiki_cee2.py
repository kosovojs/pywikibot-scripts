import pywikibot
import toolforge
import re
import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone
import time

conn = toolforge.connect('enwiki_p','analytics')

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
	(select CONCAT(gt_lat, "|", gt_lon) from geo_tags geo where geo.gt_page_id=p.page_id and gt_primary=1) as coords,
	(SELECT GROUP_CONCAT(tl_title SEPARATOR '|') FROM templatelinks            WHERE tl_title like 'Infobox%' and tl_namespace = 10 and tl_from=p.page_id) as box
	from page p
	where p.page_namespace=0 and p.page_is_redirect=0 and p.page_id in ({})"""
	
	for chunk in chunker(pages, 50):
		thispart = get_page_info_chunk(SQL,chunk)
		alldata.extend(thispart)
	#
	return alldata
#
def one_project_cats(project):
	number = "2500"# if project=="Monde antique" else "1000"
	
	SQL = """select count(l.ll_lang) as langs, ll_from
		from langlinks l
		join page p on p.page_id=l.ll_from
		where p.page_namespace IN(0)  AND p.page_is_redirect=0
		and not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
		and exists (SELECT * FROM categorylinks,page pt WHERE MOD(p.page_namespace,2)=0 AND pt.page_title=p.page_title
					AND pt.page_namespace=p.page_namespace+1
					  AND cl_from=pt.page_id AND cl_to = "{}")
		group by l.ll_from
		order by langs desc
	limit {};""".format(project.replace(' ','_'),number)
	
	query_res = run_query(SQL)
	query_res = [[encode_if_necessary(f[0]),encode_if_necessary(f[1]),project] for f in query_res]
	
	return query_res
#
def one_project_tpl(project):
	number = "2500"# if project=="Monde antique" else "1000"
	
	SQL = """select count(l.ll_lang) as langs, ll_from
		from langlinks l
		join page p on p.page_id=l.ll_from
		where p.page_namespace IN(0)  AND p.page_is_redirect=0
		and not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
		and exists (SELECT * FROM templatelinks,page pt WHERE MOD(p.page_namespace,2)=0 AND pt.page_title=p.page_title
					AND pt.page_namespace=p.page_namespace+1
					  AND tl_from=pt.page_id AND tl_namespace=10 AND tl_title = "{}")
		group by l.ll_from
		order by langs desc
	limit {};""".format(project.replace(' ','_'),number)
	
	query_res = run_query(SQL)
	query_res = [[encode_if_necessary(f[0]),encode_if_necessary(f[1]),project] for f in query_res]
	
	return query_res
#
def one_project_catsOLD(project):
	number = "2500"# if project=="Monde antique" else "1000"
	
	SQL = """select count(l.ll_lang) as langs, ll_from
		from langlinks l
		join page p on p.page_id=l.ll_from
		where not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
			and exists (select distinct pla.page_title
				from categorylinks cla
				join page pla on cla.cl_from=pla.page_id
				where pla.page_namespace=1 and cla.cl_type="page" and cla.cl_to="{}")
		group by l.ll_from
		order by count(l.ll_lang) desc
	limit {};""".format(project.replace(' ','_'),number)
	
	query_res = run_query(SQL)
	query_res = [[encode_if_necessary(f[0]),encode_if_necessary(f[1]),project] for f in query_res]
	
	return query_res
#
def one_project_tplOLD(project):
	number = "2500"# if project=="Monde antique" else "1000"
	
	SQL = """select count(l.ll_lang) as langs, ll_from
		from langlinks l
		join page p on p.page_id=l.ll_from
		where not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
			and exists (select p.page_title
						from templatelinks pl
						join page p on pl.tl_from_namespace=p.page_namespace and p.page_id=pl.tl_from
						where pl.tl_from_namespace=1 and pl.tl_title="{}")
		group by l.ll_from
		order by count(l.ll_lang) desc
	limit {};""".format(project.replace(' ','_'),number)
	
	query_res = run_query(SQL)
	query_res = [[encode_if_necessary(f[0]),encode_if_necessary(f[1]),project] for f in query_res]
	
	return query_res
#
templates = ["WikiProject_Belarus",
"WikiProject_Romania",
"WikiProject_Greece",
"WikiProject_Montenegro",
"WikiProject_Slovenia",
"WikiProject_Lithuania"]

categories = ["WikiProject_Armenia_articles",
"WikiProject_Austria_articles",
"WikiProject_Azerbaijan_articles",
"WikiProject_Bosnia_and_Herzegovina_articles",
"WikiProject_Bulgaria_articles",
"WikiProject_Czech_Republic_articles",
"WikiProject_Georgia_(country)_articles",
"WikiProject_North_Macedonia_articles",
"Moldova_articles",
"WikiProject_Serbia_articles",
"WikiProject_Slovakia_articles",
"WikiProject_Hungary_articles",
"WikiProject_Kazakhstan_articles",
"Cypriot_articles",
"WikiProject_Kosovo_articles",
"WikiProject_Turkey_articles",
"WikiProject_Estonia_articles",
"WikiProject_Poland_articles",
"WikiProject_Ukraine_articles",
"WikiProject_Russia_articles",
"Austria-Hungary_task_force_articles",
"WikiProject_Ottoman_Empire_articles",
"WikiProject_Soviet_Union_articles",
"WikiProject Albania articles",
"WikiProject Croatia articles"]

def main():
	allarticles = []
	f1 = eval(open("cee-en-allarticles-cats.txt", "r", encoding='utf-8').read())
	f2 = eval(open("cee-en-allarticles-tpls.txt", "r", encoding='utf-8').read())
	
	f1 = [f[1] for f in f1]
	f2 = [f[1] for f in f2]
	
	allarticles.extend(f1)
	allarticles.extend(f2)
	
	print(len(allarticles))
	
	allarticles = list(set(allarticles))
	
	print(len(allarticles))
	
	pageinfo = get_page_info(allarticles)
	
	with open("cee-en-allarticles-final.txt", "w", encoding='utf-8') as fileSave:
		fileSave.write(str(pageinfo))
	#
		
	#conn.close()
	pywikibot.output('done')
#
main()