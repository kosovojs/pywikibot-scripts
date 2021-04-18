import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

site = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('lvwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__meta_p')
cursor1 = connLabs.cursor()

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

SQLMAIN = """select orig.page_title, (select m2.ll_title from langlinks m2 where m2.ll_from=orig.page_id and m2.ll_lang="en")
from revision
join page orig on orig.page_id=rev_page and orig.page_is_redirect=0 and orig.page_namespace=0
where rev_timestamp>{} and rev_parent_id=0
and exists (select * from templatelinks t where orig.page_id = t.tl_from AND t.tl_namespace = 10 AND t.tl_title='Filmas_infokaste')
"""

def get_articles():
	lastRun = "{0:%Y%m%d%H%M%S}".format(get_last_run())
	query_res = run_query(SQLMAIN.format(lastRun),conn)
	
	return [[encode_if_necessary(f[0]),encode_if_necessary(f[1])] for f in query_res]
#
def get_last_run():
	query = "select lastupd from logtable where job='filmBot'"
	query_res = run_query(query,connLabs)
	
	return encode_if_necessary(query_res[0][0])
#
def set_last_run(timestamp):
	query = "UPDATE `logtable` SET lastupd=%s where job='filmBot'"
	
	timeasUTC = "{0:%Y%m%d%H%M%S}".format(timestamp)
	cursor1.execute(query, (timeasUTC))
	connLabs.commit()
#


#lastRunasString = "{0:%Y%m%d%H%M%S}".format(lastRun)

#pywikibot.output(lastRunasString)
#set_last_run(datetime.utcnow())