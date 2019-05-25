import pywikibot, re, os, requests, sys
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone
#from customFuncs import basic_petscan
from natsort import natsorted
import pymysql

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

conn = toolforge.connect_tools('s53143__lvstats_p')
conn1 = toolforge.connect('lvwiki_p')

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


file = run_query('select count(*) from page  where page_is_redirect=0 and page_namespace=0',conn1)



file = encode_if_necessary(file[0][0])
#http://pymysql.readthedocs.io/en/latest/user/examples.html

cursor = conn.cursor()

localtime2 = utc_to_local(datetime.utcnow())
dateforq12 = "{0:%Y%m%d%H%M%S}".format(localtime2)

sql2 = 'INSERT INTO `stats` (`timest`, `articles`) VALUES (%s, %s)'
cursor.execute(sql2, (dateforq12,file))

#
conn.commit()
conn.close()