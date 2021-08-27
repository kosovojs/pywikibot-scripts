import requests
import json
import urllib.parse
import pywikibot, re
import toolforge


lvsite = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('meta_p')

SQL = """SELECT dbname FROM wiki WHERE family='wikipedia' and is_closed=0
ORDER BY lang ASC;"""


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

with open("quarry_all_wikis.txt", "w", encoding='utf-8') as file:
	file.write(str(allarticles))
