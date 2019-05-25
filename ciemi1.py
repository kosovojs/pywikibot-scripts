import requests
import json
import urllib.parse
import pywikibot, re
import toolforge
from bs4 import BeautifulSoup

lvsite = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect_tools('s53143__meta_p')

SQL = """SELECT id, teksts from ciemi"""


def get_iedzsk(html):
	soup = BeautifulSoup(html, "html.parser")
	allpossibletags = soup.find_all('td',{'class':'dati_skatit'})
	
	for tag in allpossibletags:
		if 'iedz.' in tag.text:
			break
	
	return tag.text.strip()
#
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

allarticles = [[encode_if_necessary(b[0]), get_iedzsk(encode_if_necessary(b[1]))] for b in lvwiki]

with open("VISIciemi.txt", "w", encoding='utf-8') as file:
	file.write(str(allarticles))