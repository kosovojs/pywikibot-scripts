from bs4 import BeautifulSoup
import pywikibot, requests, re, os, json, urllib.parse
from urllib import parse
import pymysql
import toolforge
from customFuncs import basic_sparql

#os.chdir(r'projects/ciemi2')

#lvsite = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect_tools('s53143__meta_p')

SQL = """SELECT id, teksts from ciemi limit {} offset {}"""

def iedz_skaits(object):
	alltables = object.find_all('table')
	
	for table in alltables:
		prevtag = table.find_previous_sibling('span',{'class':'Virsr12'})
		if prevtag and 'Skaitliskais' not in prevtag.text:
			continue
			
		allelements = table.find_all('td',{'class':'dati_skatit'})
		
		toret = {}
		for element in allelements:
			prev_td = element.find_previous_sibling('td')
			if prev_td and 'Vērtība' in prev_td.text:
				toret.update({'iedzsk':element.text.strip()})
			elif prev_td and 'Apraksts' in prev_td.text:
				toret.update({'iedz_sk_datums':element.text.strip()})
		
		return toret
#


def get_param(html):
	soup = BeautifulSoup(html, "html.parser")
	allpossibletags = soup.find_all('td',{'class':'dati_skatit'})
	
	piederiba = soup.find('td',{'id':'xtpied'}).text.strip()
	#pywikibot.output(piederiba)
	
	thisdata = {}
	thisdata.update({'piederiba':piederiba})
	
	iedzskaita_dati = iedz_skaits(soup)
	thisdata.update(iedzskaita_dati)
	
	for tag in allpossibletags:
		prevtag = tag.find_previous_sibling('td')
		if prevtag:
			prevtag = prevtag.text.strip()
		else:
			prevtag = ''
		
		if tag:
			tag = tag.text.strip()
		else:
			tag = ''
			
		thisdata.update({prevtag:tag})
		
		#pywikibot.output(tag.text)
		#pywikibot.output(prevtag.text)
	#pywikibot.output(thisdata)
	
	return thisdata
#




def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(offsethere):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(SQL.format(500,offsethere))
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#


#
allarticlesreally = []


offsets = [0,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500]

for off in offsets:
	lvwiki = run_query(off)#quarry('14884','1')

	for_out = []

	allarticles = [[encode_if_necessary(b[0]), get_param(encode_if_necessary(b[1]))] for b in lvwiki]
	allarticlesreally.extend(allarticles)
#

with open("VISIciemi-2.txt", "w", encoding='utf-8') as file:
	file.write(str(allarticlesreally))