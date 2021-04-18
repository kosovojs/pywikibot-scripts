import pywikibot, os, re, requests, sys
from pywikibot.data import api
import toolforge
from datetime import timedelta, datetime

conn = toolforge.connect('lvwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__meta_p')
cursor1 = connLabs.cursor()

site = pywikibot.Site('lv', 'wikipedia')
site.login()

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

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def purge_items(titles):
	params = {
		"action": "purge",
		"format": "json",
		"forcelinkupdate": 1,
		"titles": '|'.join(titles)
	}
	
	req = api.Request(site=site, **params)
	data = req.submit()
#

SQLMAIN = """select rc_title
from recentchanges rc
join page p on p.page_id=rc.rc_cur_id and p.page_is_redirect=0
where rc_type in (1) and rc_namespace=0 and rc_timestamp>{}
"""

def get_last_run():
	query = "select lastupd from logtable where job='purge'"
	query_res = run_query(query,connLabs)
	
	return encode_if_necessary(query_res[0][0])
#
def set_last_run(timestamp):
	query = "UPDATE `logtable` SET lastupd=%s where job='purge'"
	
	timeasUTC = "{0:%Y%m%d%H%M%S}".format(timestamp)
	cursor1.execute(query, (timeasUTC))
	connLabs.commit()
#

def get_articles():
	lastRun = "{0:%Y%m%d%H%M%S}".format(get_last_run())
	query_res = run_query(SQLMAIN.format(lastRun),conn)
	
	return [encode_if_necessary(f[0]) for f in query_res]
#
def main():
	#articles= [f for f in filmlist.split('\n') if len(f)>3]#
	#articlelist = ['','']
	thelist = get_articles()
	
	for group in chunker(thelist,40):
		purge_items(group)
	
	set_last_run(datetime.utcnow())
		
main()