import pywikibot, re, os, collections, sys
from customFuncs import get_quarry as quarry
from natsort import natsorted
import toolforge
from datetime import datetime

#os.chdir(r'projects/treisijs2')

IWlimit = 48

SQL = """SELECT ips_item_id, COUNT(ips_item_id), (SELECT GROUP_CONCAT(distinct concat(wb1.ips_site_id, '-frkmarker-',wb1.ips_site_page) separator '|') as 'otherlinks'
										 FROM wb_items_per_site wb1
										 WHERE wb1.ips_site_id in ('enwiki','dewiki','eswiki','ruwiki','frwiki') and wb1.ips_item_id=www.ips_item_id) as 'other links'
FROM wb_items_per_site www
WHERE ips_site_id LIKE '%wiki'
AND NOT ips_site_id='wikidatawiki'
AND NOT ips_site_id='commonswiki'
GROUP BY ips_item_id 
HAVING COUNT(ips_item_id) > 47
AND ips_item_id NOT IN
(SELECT ips_item_id
FROM wb_items_per_site
WHERE ips_site_id='lvwiki')
ORDER BY COUNT(ips_item_id) DESC;"""

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def sql_big_query():
	print('Started at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	conn = toolforge.connect('meta_p')

	#try:
	with conn.cursor() as cur:
		cur.execute("SELECT dbname FROM wiki WHERE family='wikipedia' and is_closed=0")
		rows = cur.fetchall()

		print('Query ended at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		quaryrun1 = []
	
		for one in rows:
			quaryrun1.append([encode_if_necessary(b) for b in one])
	
		filsess1 = open('treisijs-big-query12121212.txt','w', encoding='utf-8')
		filsess1.write(str(quaryrun1))
	#except:
	#	print('Exception at: '+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
sql_big_query()