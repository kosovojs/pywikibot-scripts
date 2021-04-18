import pywikibot, re, os, collections, sys
from customFuncs import get_quarry as quarry
from natsort import natsorted
import toolforge
from datetime import datetime

MAX_ID = 83737550#SELECT max(ips_item_id) FROM wb_items_per_site

ONE_STEP = 100000

parts = [[i+1, i + ONE_STEP] for i in range(0, MAX_ID, ONE_STEP)]

#os.chdir(r'projects/treisijs2')

IWlimit = 47

SQL = """SELECT ips_item_id, COUNT(ips_item_id)
FROM wb_items_per_site www
WHERE ips_item_id between {} and {}
and ips_site_id RLIKE 'wiki$'
AND (NOT ips_site_id='wikidatawiki'
     AND NOT ips_site_id='commonswiki')
GROUP BY ips_item_id 
HAVING COUNT(ips_item_id) > 47"""


""" AND ips_item_id NOT in
(SELECT inn.ips_item_id
FROM wb_items_per_site inn
WHERE inn.ips_site_id='lvwiki' and inn.ips_item_id between {} and {}) """

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def sql_big_query():
	print('Started at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)
	conn = toolforge.connect('wikidatawiki_p','analytics')

	#try:
	with conn.cursor() as cur:
		for onePart in parts[150:157]:
			print('Query started at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)
			cur.execute(SQL.format(onePart[0],onePart[1]))#,onePart[0],onePart[1]
			rows = cur.fetchall()

			print('Query ended at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)
			quaryrun1 = []
		
			for one in rows:
				quaryrun1.append([encode_if_necessary(b) for b in one])
		
			filsess1 = open('treisijs-big-query12121212-wo-lv-'+str(onePart[0])+'.txt','w', encoding='utf-8')
			filsess1.write(str(quaryrun1))
	#except:
	#	print('Exception at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)
#
sql_big_query()
