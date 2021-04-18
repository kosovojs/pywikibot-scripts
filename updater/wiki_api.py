import yaml
import os
import json
from pywikiapi import wikipedia
from re import search
from helpers import chunker, saveToFile

badvals = ['Q11266439','Q4167836','Q4167410']
langFallback = ['en','de','ru']

config = yaml.safe_load(open('config.yaml'))

class WikiAPI:
	wdSite = None
	itemData_FULL = {}
	itemData = {}
	allLanguages = []

	def getBestSiteAndDesc(self, data):
		bestDesc = ''
		bestSite = []

		for lang in langFallback:
			if lang in data['descriptions']:
				bestDesc = data['descriptions'][lang]
				break

		for lang in langFallback:
			if lang in data['sitelinks']:
				bestSite = [lang, data['sitelinks'][lang]]
				break
		
		return {'desc': bestDesc, 'site': bestSite}

	def oneBatch(self, items, makeAPICall = True):
		if makeAPICall:
			apiData = self.wdSite("wbgetentities", props="sitelinks|descriptions|claims", ids=items,redirects='yes')['entities']
		else:
			apiData = items
			
		for entity in apiData:
			data = apiData[entity]

			if makeAPICall:
				descs = data['descriptions']
				sitelinks = data['sitelinks']
				claims = data['claims']

				formattedData = {
					'sitelinks': {wiki:sitelinks[wiki]['title'] for wiki in sitelinks if wiki in self.allLanguages},
					'descriptions': {val:descs[val]['value'] for val in descs},
					'p31': [f["mainsnak"]["datavalue"]["value"]["id"] for f in claims['P31']] if 'P31' in claims else [],
					'p279': [f["mainsnak"]["datavalue"]["value"]["id"] for f in claims['P279']] if 'P279' in claims else []
				}

				self.itemData_FULL.update({entity: formattedData})
			else:
				formattedData = data

			if self.ifOKItem(formattedData):
				bestData = self.getBestSiteAndDesc(formattedData)
				self.itemData.update({entity: {'formatted': formattedData, 'best': bestData, 'iws': len(formattedData['sitelinks'])}})
	
	def ifOKItem(self, data):
		for sitel in data['sitelinks']:
			currSitel = data['sitelinks'][sitel]
			if currSitel.startswith(('Category:','Categoría:','Категория:','Kategorie:','Catégorie:','Vorlage:','Plantilla:','Шаблон:','Template:','Wikipedia:','Википедия:','Portal:','Hilfe:','Help:','Mediawiki:','MediaWiki:','Module:')):
				return False

		if any([f for f in badvals if f in data['p31']]):
			return False

		if 'en' in data['sitelinks']:
			if search('^(AD )?\d+(s|s \(decade\))?( BC)?$',data['sitelinks']['en'].replace('_', ' ')):
				return False

		return True

	def getWikidataItems(self, allItems):
		self.fetchWikipediaLanguages()
		self.wdSite = wikipedia('www','wikidata')
		
		filename = config['filename-api']

		if os.path.isfile(filename):
			data = eval(open(filename,'r',encoding='utf-8').read())
			self.oneBatch(data,False)
		else:
			for group in chunker(allItems,50):
				self.oneBatch(group)
			
			saveToFile(filename, json.dumps(self.itemData_FULL, ensure_ascii=False))

	def fetchWikipediaLanguages(self):
		site = wikipedia('en')

		apiRes = site('sitematrix', smtype='language', smstate='all', smlangprop='code|name|site|dir|localname', smsiteprop='dbname|code|sitename|url|lang', smlimit='max')['sitematrix']

		#print(apiRes)

		for ind in apiRes:
			if ind == 'count':
				continue
			#{'code': 'zu', 'name': 'isiZulu', 'site': [{'url': 'https://zu.wikipedia.org', 'dbname': 'zuwiki', 'code': 'wiki', 'lang': 'zu', 'sitename': 'Wikipedia'}, {'url': 'https://zu.wiktionary.org', 'dbname': 'zuwiktionary', 'code': 'wiktionary', 'lang': 'zu', 'sitename': 'Wiktionary'}, {'url': 'https://zu.wikibooks.org', 'dbname': 'zuwikibooks', 'code': 'wikibooks', 'lang': 'zu', 'sitename': 'Wikibooks', 'closed': True}], 'dir': 'ltr', 'localname': 'zulu'}
			data = apiRes[ind]
			#print(ind)
			#languageCode = data['site']['dbname']#data['code']
			foundWiki = False
			
			for site in data['site']:
				if 'closed' in site and site['closed'] == True:
					continue
				
				if site['code'] == 'wiki':
					languageCode = site['dbname']
					self.allLanguages.append(languageCode)
					break
#

if __name__ == '__main__':
	inst = WikiAPI()
	res = inst.getWikidataItems(['Q15912205','Q3168'])
	print(inst.itemData)