import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

site = pywikibot.Site("en", "wikipedia")
conn = toolforge.connect('frwiki_p','analytics')
#connLabs = toolforge.connect_tools('s53143__mis_lists_p')
#cursor1 = connLabs.cursor()

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
SQL_main = """select count(l.ll_lang) as langs, p.page_title, (select m2.ll_title from langlinks m2 where m2.ll_from=l.ll_from and m2.ll_lang="en")  as en, (select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd{}
from langlinks l
join page p on p.page_id=l.ll_from
and p.page_namespace=0 and not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
	and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
               										and cla.cl_to="Portail:{}/Articles_liés"
               )
group by l.ll_from
having count(l.ll_lang)>20
order by count(l.ll_lang) desc;"""

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
	#{'group':'other','name':'Berlīne','frwiki':'Berlin'},
	#{'group':'other','name':'DĀR','frwiki':'Afrique_du_Sud'},
	#{'group':'other','name':'Japāna','frwiki':'Japon'},
	{'group':'other','name':'Irāna','frwiki':'Iran'},
	{'group':'other','name':'Irāka','frwiki':'Irak'},
	#{'group':'other','name':'Āfrika','frwiki':'Afrique'},
	#{'group':'other','name':'Senā pasaule','frwiki':'Monde antique'},
	#{'group':'other','name':'Senā Ēģipte','frwiki':'Égypte antique'},
	#{'group':'other','name':'indija','frwiki':'Monde_indien'},
	#{'group':'','name':'','frwiki':''},
	#{'group':'','name':'','frwiki':''},
	#{'group':'','name':'','frwiki':''},
]

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def get_page_info_chunk(SQL,additional,pages):
	query_res = run_query(SQL.format(additional,', '.join(map(str,pages))))
	query_res = [encode_all_items(f) for f in query_res]
	
	query_res = {f[0]:f[1:] for f in query_res}
	
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
		
		infs = infobox.split('|')
		
		if 'Infobox_Subdivision_administrative' in infs: return False
		if 'Infobox_Biographie2' in infs: return False
		if 'Infobox_Politicien' in infs: return False
	elif project == "japon":
		infoboxes = page_data[3].replace('_',' ')
		if not infoboxes:
			infoboxes = ""
		
		infs = infobox.split('|')
		
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
def get_page_info(project,pages):
	alldata = {}
	addit = ""
	
	SQL = """select page_id, page_title,
	(select m2.ll_title from langlinks m2 where m2.ll_from=p.page_id and m2.ll_lang="en")  as en,
	(select pp.pp_value from page_props pp where pp.pp_page=p.page_id and pp_propname='wikibase_item') as wd{}
	from page p
	where p.page_namespace=0 and p.page_is_redirect=0 and p.page_id in ({})"""
	
	if project=='Monde_indien':
		addit = ",    (SELECT GROUP_CONCAT(tl_title SEPARATOR '|') FROM templatelinks            WHERE tl_title like 'Infobox%' and tl_namespace = 10 and tl_from=p.page_id) as box"
	
	for chunk in chunker(pages, 50):
		thispart = get_page_info_chunk(SQL,addit,chunk)
		alldata.update(thispart)
	#
	return alldata
#
def one_project(project):
	number = "2000" if project=="Monde antique" else "1000"
	
	SQL = """select count(l.ll_lang) as langs, ll_from
		from langlinks l
		where not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
			and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
															and cla.cl_to="Portail:{}/Articles_liés"
					   )
		group by l.ll_from
		order by count(l.ll_lang) desc
	limit {};""".format(project.replace(' ','_'),number)
	
	query_res = run_query(SQL)
	query_res = [encode_all_items(f) for f in query_res]
	
	page_ids = {f[1]:f[0] for f in query_res}
	
	page_info = get_page_info(project,list(page_ids))
	
	finaldata, errors = merge_res(page_ids,page_info,project)
	
	finaldata = str(json.dumps(finaldata[:800]))#finaldata[:800]
	
	#with open("tokija-ex.txt", "w", encoding='utf-8') as file1:
	#	file1.write(str(finaldata))
	return finaldata
#
def insert_into_db(group_name,name,jsondata):
	sql_insert = 'INSERT INTO `entries` (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'
	sql_update = 'UPDATE `entries` SET jsondata=%s, last_upd=%s where group_name=%s and name=%s'
	
	curr_time = utc_to_local(datetime.utcnow())
	dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
	
	connLabs = toolforge.connect_tools('s53143__mis_lists_p')
	cursor1 = connLabs.cursor()
	
	isAlreadyInDB_sql = 'select id from entries where group_name=%s and name=%s'
	
	cursor1.execute(isAlreadyInDB_sql, (group_name,name))
	isAlreadyInDB = cursor1.fetchall()
	
	#cursor1.execute(sql_insert, (infobox.replace('Infobox_','').replace('_',' '), 'eninfobox',str(json.dumps(result_json)),dateforq1))
	if len(isAlreadyInDB)<1:
		cursor1.execute(sql_insert, (name, group_name,jsondata,dateforq1))
	else:
		cursor1.execute(sql_update, (jsondata,dateforq1,group_name, name))
		
	connLabs.commit()
	connLabs.close()
#

def main():
	#infoboxlist = get_input_list()
	
	for infobox in jsoninput:
		infname = infobox['name']
		fr = infobox['frwiki']
		grupa = infobox['group']
		pywikibot.output('\t'+infname)
		
		result_json = one_project(fr)
		insert_into_db(grupa,infname,result_json)
		
	conn.close()
	pywikibot.output('done')
#
main()