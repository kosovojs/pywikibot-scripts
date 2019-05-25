import pywikibot, re, json, os, time, requests
from datetime import datetime
import sqlite3 as lite
import sys
import re, os, sys, pywikibot, toolforge

connLabs = toolforge.connect_tools('s53143__meta_p')
cursor1 = connLabs.cursor()

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection = connLabs):
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

def get_info_from_db():
	query = 'select id from ciemi where teksts="" limit 1'
	query_res = run_query(query,connLabs)
	
	if len(query_res)>0:
		return query_res[0][0]
	else:
		return False
	#print(data)
#
def do_one(nr):
	url = "http://vietvardi.lgia.gov.lv/vv/to_www_obj.objekts?p_id={}".format(nr)
	
	url2= requests.get(url)
	url2.encoding = 'Windows-1257'
	top250_source = str(url2.text)
	#titulo_unicode = top250_source.decode('utf8')
	#pywikibot.output(top250_source)
	nr = str(nr)
	
	query = "UPDATE `ciemi` SET teksts=%s where id=%s"
	cursor1.execute(query, (top250_source,nr))
	connLabs.commit()
#
def main():
	hasmoredata = True
	counter = 0
	begintime = time.time()
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	while hasmoredata:
		try:
			infodata = get_info_from_db()
			if not infodata:
				hasmoredata = False
				break
			
			counter += 1
			if counter % 50 == 0:
				print('\t\t'+str(counter))
				sys.stdout.flush()
			
			#if counter==2:
			#	hasmoredata = False
				
			item = infodata
			do_one(item)
			time.sleep(2)
		except:
			print('final except')
			hasmoredata = False
	#
	#con.close()
	print('Done!')
	endtime = time.time()
	print('it took: {}'.format((endtime-begintime)))
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#
main()