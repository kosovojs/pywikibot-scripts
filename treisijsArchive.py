import pywikibot, re, os, requests, sys
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone
#from customFuncs import basic_petscan
from natsort import natsorted
import pymysql

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

conn = toolforge.connect_tools('s53143__missing_p')
conn1 = toolforge.connect('lvwiki_p','analytics')

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

def local_to_utc(utc):
	return lva_timezone.localize(utc).astimezone(utc_timezone)
#
def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection):
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

currWDitemsQuery = run_query("select pp_value from page_props where pp_propname='wikibase_item'",conn1)
currWDitems = [int(encode_if_necessary(b[0])[1:]) for b in currWDitemsQuery]
#print(currWDitems)

treisijsListQuery = run_query("SELECT wd from articles where archived is null",conn)
treisijsList = [encode_if_necessary(b[0]) for b in treisijsListQuery]
#print(treisijsList)

createdArticles = list(set(currWDitems) & set(treisijsList))

if len(createdArticles) < 1:
	print('no cretaed articles')
	#return;
else:
	#
	updateQuery = "UPDATE articles SET archived = 1 where wd in ({})".format(', '.join(map(str,createdArticles)))
	print(updateQuery)

	cursor = conn.cursor()

	cursor.execute(updateQuery)

	conn.commit()
	conn.close()
