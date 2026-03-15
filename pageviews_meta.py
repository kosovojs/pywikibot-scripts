import requests
import json
import urllib.parse
#import pywikibot, re
import toolforge

#lvsite = pywikibot.Site("lv", "wikipedia")
lv_conn = toolforge.connect('lvwiki_p')
et_conn = toolforge.connect('etwiki_p')

redirects = """select p1.page_id redirect_page_id, p1.page_title as redirect_page, rd_title as redirect_target, p2.page_id as target_page_id
from redirect
join page p1 on p1.page_id=rd_from and p1.page_namespace=0
join page p2 on p2.page_title=rd_title and p2.page_namespace=0 and p2.page_is_redirect=0
where rd_namespace=0"""

pages = """select page_id, page_title
from page
where page_namespace=0 and page_is_redirect=0"""

def decode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(conn, query):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		exit()

	return rows
#

for wiki in ['lv', 'et']:
	if wiki == 'lv':
		conn = lv_conn
	else:
		conn = et_conn

	print(f"Processing {wiki}wiki - redirects")
	reds = [[decode_if_necessary(entry[0]), decode_if_necessary(entry[1]), decode_if_necessary(entry[2]), decode_if_necessary(entry[3])] for entry in run_query(conn, redirects)]

	with open(f"pageviews2025-{wiki}-redirects.txt", "w", encoding='utf-8') as file:
		file.write(json.dumps(reds, ensure_ascii=False))

	print(f"Processing {wiki}wiki - articles")
	articles = [[decode_if_necessary(entry[0]), decode_if_necessary(entry[1])] for entry in run_query(conn, pages)]

	with open(f"pageviews2025-{wiki}-articles.txt", "w", encoding='utf-8') as file:
		file.write(json.dumps(articles, ensure_ascii=False))
