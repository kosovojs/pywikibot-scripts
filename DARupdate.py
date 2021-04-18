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
	{'group':'other','name':'Berlīne','frwiki':'Berlin'},
	{'group':'other','name':'DĀR','frwiki':'Afrique_du_Sud'},
	{'group':'other','name':'indija','frwiki':'Monde_indien'},
	#{'group':'','name':'','frwiki':''},
	#{'group':'','name':'','frwiki':''},
	#{'group':'','name':'','frwiki':''},
]

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def main():
	#infoboxlist = get_input_list()
	
	for infobox in jsoninput:
		infname = infobox['name']
		fr = infobox['frwiki']
		grupa = infobox['group']
		pywikibot.output('\t'+infname)
		
		sys.stdout.flush()
		begin = time.time()
		#result_json = []
		appending = ''
		if infname=='indija':
			appending = ",    (SELECT GROUP_CONCAT(tl_title SEPARATOR '|') FROM templatelinks            WHERE tl_title like 'Infobox%' and tl_namespace = 10 and tl_from=p.page_id) as box"
		query_res = run_query(SQL_main.format(appending,fr))
		
		end = time.time()
		timelen = end-begin
		if timelen>30:
			pywikibot.output('{}'.format(timelen))
		
		result_json = format_frwiki(infname,[encode_all_items(f) for f in query_res])
		curr_time = utc_to_local(datetime.utcnow())
		dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
		#print(dateforq1)
		
		#put_db(infobox,result_json,dateforq1)
		#cursor1.execute(sql_insert, (infobox.replace('Infobox_','').replace('_',' '), 'eninfobox',str(json.dumps(result_json)),dateforq1))
		
		#pywikibot.output(SQL_main.format(newtitle))
		pywikibot.output(result_json)
		#if not connLabs and not connLabs.open:
		connLabs = toolforge.connect_tools('s53143__mis_lists_p')
		cursor1 = connLabs.cursor()
		
		cursor1.execute(sql_update, (str(json.dumps(result_json)),dateforq1,grupa, infname))
		
		connLabs.commit()
		
		connLabs.close()
	conn.close()
	pywikibot.output('done')
		
#
main()