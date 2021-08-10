
from pywikiapi import wikipedia
from helpers import clean_api, chunker
import os, pymysql, json, re
# Connect to English Wikipedia

class WikidataAPI:
	site = None

	def __init__(self):
		self.site = wikipedia('www', 'wikidata')

	def get_item_data(self, wd_items, raw=False, attributes = ['sitelinks', 'claims'], claim_props=[]):

		retMap = {}

		for batch in chunker(wd_items, 49):
			res = self.site('wbgetentities', ids=batch, props='|'.join(attributes))
			for entity in res.get('entities'):
				data = res.get('entities').get(entity)
				tmp_data = {}
				for attr in attributes:
					if attr == 'sitelinks':
						sitelinks = {f:data.get(attr).get(f).get('title') for f in data.get(attr)}
						data.update({'sitelinks': sitelinks})
					if attr == 'claims':
						claims = clean_api(data.get(attr))
						data.update({'claims': claims})
				#print(data.get('type'))
				#parsed_data = clean_api(data) if raw and 'claims' else data

				retMap.update({entity: data})

		return retMap
