from petscan import Petscan
import pymysql, os, json, re, requests
from helpers import get_label, wplist
from wd_api import WikidataAPI
from logger import logger
from pywikiapi import wikipedia

class MissingArticlesHandler:
	missing_wiki = None

	def __init__(self, missing_wiki):
		self.missing_wiki = missing_wiki
		self.wd_client = WikidataAPI()
		self.petscan = Petscan()

	def get_sitelinks(self, wikidata_item):
		item_data = self.wd_client.get_item_data([wikidata_item],
												 attributes=['sitelinks'])
		sitelinks = item_data.get(wikidata_item).get('sitelinks')
		listing = [[f, sitelinks.get(f)] for f in sitelinks if f in wplist]

		return listing

	def get_wd_items_from_wiki_category(self, language, category, depth):
		MIS_IW_LIMIT = 5
		payl = {
			'categories': category,
			'language': language,
			'project': 'wikipedia',
			'doit': 'Do it!',
			'format': 'json',
			'common_wiki': 'auto',
			'depth': depth,
			'output_compatability': 'catscan',
			'sitelinks_no': 'lvwiki',
			'ns[0]': '1',
			'combination': 'subset',
			'wikidata_item': 'any',
			'min_sitelink_count': MIS_IW_LIMIT
		}

		return self.petscan.get_data(json=payl, return_type='wd')


	def format_data_for_report(self, data):
		label, lang = get_label(data.get('sitelinks'), ['en'])

		iw_count = len(set(data.get('sitelinks'))&wplist)
		image = data.get('claims', {}).get('P18')
		dob = data.get('claims', {}).get('P569')
		gender = data.get('claims', {}).get('P21')

		return dict(label=label, label_lang=lang, iw_count=iw_count,image=image, dob=dob, gender=gender)

	def handle_all_wikis(self, wikidata_item, depth=0):
		#logger.warning(f'checking all missing articles for wd item: {wikidata_item}')
		wikis = self.get_sitelinks(wikidata_item)

		wd_items = []
		#logger.warning(f'found wikis: {len(wikis)}')

		for wikipedia, category in wikis:
			wikipedia = wikipedia.replace('wiki', '')
			category = category.partition(':')[2]
			curr = self.get_wd_items_from_wiki_category(
				wikipedia, category, depth)
			wd_items.extend(curr)
		wd_items = list(set(wd_items))

		#logger.warning(f'found wikidata items: {len(wd_items)}')
		wd_data = self.wd_client.get_item_data(wd_items, attributes=['claims', 'sitelinks'])

		formateed = {}

		for entry in wd_data:
			report_data = self.format_data_for_report(wd_data.get(entry))
			formateed.update({entry:report_data})

		with open('test.json', 'w', encoding='utf-8') as file_w:
			file_w.write(json.dumps(formateed, ensure_ascii=False, indent=4, sort_keys=True))

		return formateed

	def handle_subcategories(self, wiki, category, depth=0):
		wd_items = self.get_wd_items_from_wiki_category(wiki.replace('wiki', ''), category, depth)

		#logger.warning(f'found wikidata items: {len(wd_items)}')
		wd_data = self.wd_client.get_item_data(wd_items, attributes=['claims', 'sitelinks'])

		formateed = {}

		for entry in wd_data:
			report_data = self.format_data_for_report(wd_data.get(entry))
			formateed.update({entry:report_data})

		return formateed

	#category - has to be with "category:" namespace
	def subcats(self, wiki, category):
		site = wikipedia(wiki.replace('wiki', ''))
		categories = []
		for r in site.query(list='categorymembers',cmtitle=category, cmlimit= "500"):
			for cat in r.categorymembers:
				ns = cat.get('ns')
				if ns != 14: continue

				categories.append(cat.get('title'))

		mapp = {}

		for category in categories:
			print(category)
			category = category.partition(':')[2]

			formateed = self.handle_subcategories(wiki.replace('wiki', ''), category, 1)

			mapp.update({category: formateed})

		with open('test1.json', 'w', encoding='utf-8') as file_w:
			file_w.write(json.dumps(mapp, ensure_ascii=False, indent=4, sort_keys=True))

		return mapp
