import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

site = pywikibot.Site("en", "wikipedia")
conn = toolforge.connect('enwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__mis_lists_p')
cursor1 = connLabs.cursor()

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
SQL_main = """select p.page_title, count(l.ll_lang) as langs,
	(select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd
from langlinks l
join page p on p.page_id=l.ll_from
where  l.ll_from in (select tl.tl_from from templatelinks tl where tl.tl_title="{}" and tl_namespace=10 and tl.tl_from_namespace=0)
and p.page_namespace=0 and l.ll_from not in (select m.ll_from from langlinks m where m.ll_lang="lv")
group by l.ll_from
order by count(l.ll_lang) desc
limit 1000;"""


def get_input_list():
	data = run_query('select id, name from entries where group_name="eninfobox"',connLabs)
	data = [encode_all_items(f) for f in data]
	
	return data
#
def check_title(curr):
	currtitle = 'Template:Infobox {}'.format(curr)
	
	if curr =='adult biography': return 'Infobox_{}'.format(curr).replace(' ','_')
	
	pagetosave = pywikibot.Page(site,currtitle)
	
	if not pagetosave.exists(): return False
	
	if pagetosave.isRedirectPage():
		pagetosave = pagetosave.getRedirectTarget()
	
	return pagetosave.title().replace('Template:','').replace(' ','_')#.replace('Infobox','').replace('_',' ').strip()
#
def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

#infoboxlist = infoboxlist[::-1]

#sql_insert = 'UPDATE `entries` INTO (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'
sql_update = 'UPDATE `entries` SET jsondata=%s, last_upd=%s, name=%s where id=%s'

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def main():
	infoboxlist = get_input_list()
	
	for infobox in infoboxlist:
		infid, infname = infobox
		pywikibot.output('\t'+infname)
		
		newtitle = check_title(infname)
		if not newtitle: continue
		
		if newtitle in ('Infobox_person'):
			pywikibot.output(infname)
			continue
		
		pywikibot.output(newtitle)
		
		sys.stdout.flush()
		begin = time.time()
		#result_json = []
		query_res = run_query(SQL_main.format(newtitle))
		
		end = time.time()
		timelen = end-begin
		if timelen>30:
			pywikibot.output('{}'.format(timelen))
		
		result_json = [encode_all_items(f) for f in query_res]
		curr_time = utc_to_local(datetime.utcnow())
		dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
		#print(dateforq1)
		
		#put_db(infobox,result_json,dateforq1)
		#cursor1.execute(sql_insert, (infobox.replace('Infobox_','').replace('_',' '), 'eninfobox',str(json.dumps(result_json)),dateforq1))
		
		#pywikibot.output(SQL_main.format(newtitle))
		pywikibot.output(result_json[:3])
		cursor1.execute(sql_update, (str(json.dumps(result_json)),dateforq1,infname.replace('Infobox_','').replace('_',' '), infid))
		
		connLabs.commit()
	connLabs.close()
	conn.close()
	pywikibot.output('done')
		
#
main()