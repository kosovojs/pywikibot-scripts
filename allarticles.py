import requests
import json
import urllib.parse
import pywikibot, re, sys
import toolforge

lvsite = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('lvwiki_p')

SQL = """Select page_title
from page where page_namespace=0"""# and page_is_redirect=0


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

allarticles = [encode_if_necessary(b[0]).replace('_',' ') for b in lvwiki]

with open("quarry_results_links_lv.txt", "w", encoding='utf-8') as file:
	file.write(str(allarticles))