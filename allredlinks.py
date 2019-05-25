import requests
import json
import urllib.parse
import pywikibot, re
import toolforge

lvsite = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('lvwiki_p','analytics')

SQL = """SELECT l.pl_from, l.pl_namespace, l.pl_title
FROM pagelinks l
INNER JOIN page f ON f.page_id = l.pl_from
LEFT OUTER JOIN page t ON t.page_namespace = l.pl_namespace AND t.page_title = l.pl_title
WHERE f.page_namespace = 0 and l.pl_namespace=0
	AND   t.page_id IS NULL"""


def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query():
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(SQL)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#
lvwiki = run_query()#quarry('14884','1')

for_out = []

allarticles = ["\t".join([str(encode_if_necessary(f)) for f in b]) for b in lvwiki]

with open("quarry_results_links_lv-reds.txt", "w", encoding='utf-8') as file:
	file.write('\n'.join(allarticles))