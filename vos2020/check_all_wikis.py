from petscan import Petscan
import pymysql, os, json, re, requests
from helpers import get_label, wplist
from wd_api import WikidataAPI
from pywikiapi import wikipedia
from logger import logger

wd_client = WikidataAPI()
petscan = Petscan()

def get_sitelinks(wikidata_item):
	item_data = wd_client.get_item_data([wikidata_item],
												attributes=['sitelinks'])
	sitelinks = item_data.get(wikidata_item).get('sitelinks')
	listing = [[f, sitelinks.get(f)] for f in sitelinks if f in wplist]

	return listing

def page_exists(wiki, title):
	if wiki == 'be_x_oldwiki':
		wiki = 'be-taraskwiki'
	site = wikipedia(wiki.replace('wiki', ''))
	res = site.query(titles=[title])
	for r in res:
		for page in r.pages:
			if page.get('missing'):
				return False

	return True


vos2020 = [f[0] for f in get_sitelinks('Q66827758')]

lst = []

data = [
	[2008, 'Q7135667'],
	[2012, 'Q7140914'],
	[2016, 'Q24335239'],
]

for year,wd in data:
	vos2016 = get_sitelinks(wd)
	logger.debug(f'year: {year}, wikis: {len(vos2016)}')
	for wiki, cat in vos2016:
		if wiki in vos2020:
			continue
		repl = cat.replace(str(year), '2020')


		if page_exists(wiki, repl):
			lst.append([wiki, repl])

with open('test2020.json', 'w', encoding='utf-8') as file_w:
	file_w.write(json.dumps(lst, ensure_ascii=False, indent=4, sort_keys=True))
