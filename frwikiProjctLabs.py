import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

conn = toolforge.connect('frwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__mis_lists_p')
cursor1 = connLabs.cursor()

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

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
SQL_main = """select count(l.ll_lang), p.page_title, (select m2.ll_title from langlinks m2 where m2.ll_from=l.ll_from and m2.ll_lang="en")
from langlinks l
join page p on p.page_id=l.ll_from
and p.page_namespace=0 and not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
	and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
               										and cla.cl_to="Portail:Berlin/Articles_liés"
               )
group by l.ll_from
order by count(l.ll_lang) desc
limit 1000;"""

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

sql_insert = 'INSERT INTO `entries` (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'

def format_frwiki(data):
	ret = []
	for row in data:
		langs,fr,en = row
		if en!='':
			ret.append([en,langs,""])
		else:
			pywikibot.output(row)
	return ret

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def main():
	#for infobox in infoboxlist:
	#	pywikibot.output('\t'+infobox)
	#	sys.stdout.flush()
	begin = time.time()
	#result_json = []
	query_res = run_query(SQL_main)
	
	end = time.time()
	timelen = end-begin
	if timelen>30:
		pywikibot.output('{}'.format(timelen))
	
	result_json = format_frwiki([encode_all_items(f) for f in query_res])
	curr_time = utc_to_local(datetime.utcnow())
	dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
	#print(dateforq1)
	
	#put_db(infobox,result_json,dateforq1)
	cursor1.execute(sql_insert, ('Berlīne', 'other',str(json.dumps(result_json)),dateforq1))
	
	connLabs.commit()
	connLabs.close()
	conn.close()
	pywikibot.output('done')
		
#
main()