import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

site = pywikibot.Site("en", "wikipedia")
conn = toolforge.connect('enwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__mis_lists_p')
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
SQL_main = """select p.page_title, count(l.ll_lang)
from langlinks l
join page p on p.page_id=l.ll_from
where exists (select * from pagelinks pl
						join page p on p.page_title=pl.pl_title and pl.pl_namespace=p.page_namespace
						where p.page_id=l.ll_from and pl.pl_from={} and pl.pl_namespace=0)
and p.page_namespace=0 and not exists (select * from langlinks m where l.ll_from=m.ll_from and m.ll_lang="lv")
group by l.ll_from
order by count(l.ll_lang) desc;"""

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

#infoboxlist = infoboxlist[::-1]

#sql_insert = 'UPDATE `entries` INTO (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'
sql_update = 'UPDATE `vital` SET jsondata=%s, last_upd=%s where pageId=%s'

def get_input_list():
	data = run_query('select pageId from vital where pageId is not null',connLabs)
	data = [encode_if_necessary(f[0]) for f in data]
	
	return data
#
def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def main():
	infoboxlist = get_input_list()
	
	for infobox in infoboxlist:
		begin = time.time()
		query_res = run_query(SQL_main.format(infobox))
		
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
		#pywikibot.output(result_json)
		#if not connLabs and not connLabs.open:
		connLabs = toolforge.connect_tools('s53143__mis_lists_p')
		cursor1 = connLabs.cursor()
		
		cursor1.execute(sql_update, (str(json.dumps(result_json)),dateforq1,infobox))
		
		connLabs.commit()
		
		connLabs.close()
	conn.close()
	pywikibot.output('done')
		
#
main()