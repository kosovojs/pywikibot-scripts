import requests
import json
import urllib.parse
import pywikibot, re
import toolforge

lvsite = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('lvwiki_p')

SQL = """SELECT distinct eu_entity_id
from page p
join wbc_entity_usage wb on p.page_id=wb.eu_page_id
where p.page_namespace=0 and p.page_is_redirect=0"""


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

allarticles = [encode_if_necessary(b[0]) for b in lvwiki]

with open("lvWDitems.txt", "w", encoding='utf-8') as file:
	file.write(str(allarticles))