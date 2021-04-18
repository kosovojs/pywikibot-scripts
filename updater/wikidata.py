import toolforge
import os
import os.path
import pymysql
import yaml
import json

from helpers import saveToFile, encode_if_necessary

SQL_MAIN_TEMPLATE = """SELECT ips_item_id, COUNT(ips_item_id)
FROM wb_items_per_site www
WHERE ips_site_id RLIKE 'wiki$'
AND NOT ips_site_id='wikidatawiki'
AND NOT ips_site_id='commonswiki'
GROUP BY ips_item_id 
HAVING COUNT(ips_item_id) > {}
ORDER BY COUNT(ips_item_id) DESC"""

SQL_EXISTING_ITEMS_TEMPLATE = """SELECT ips_item_id
FROM wb_items_per_site
WHERE ips_site_id='{}wiki'"""

config = yaml.safe_load(open('config.yaml'))

class Wikidata:
	conn = None
	mainData = {}
	langData = {}
	langLists = {}
	goodItems = []

	def __init__(self):
		self.connect()
	
	def connect(self):
		if config['dev']:
			pass
		else:
			self.conn = pymysql.connect( database='wikidatawiki_p', host='wikidatawiki.analytics.db.svc.eqiad.wmflabs', read_default_file=os.path.expanduser("~/replica.my.cnf"), charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

	def runQuery(self, sql: str, params: tuple = (), maxTries: int = 2) -> dict:
		with self.conn.cursor() as cursor:
			cursor.execute(sql, params)
			result = cursor.fetchall()
			return result
	
	def loadFromFile(self):
		fileHandler = eval(open(config['main-query']['filename'],'r',encoding='utf-8').read())

		return fileHandler

	def handleMainQuery(self):
		fullSQL = SQL_MAIN_TEMPLATE.format(config['main-query']['min-langs'])

		queryData = self.runQuery(fullSQL)

		finalData = []

		for row in queryData:
			finalData.append([encode_if_necessary(b) for b in row])
		
		saveToFile(config['main-query']['filename'], json.dumps(finalData, ensure_ascii=False))

		return finalData

	def getMainData(self):
		doNeedToUseCache = config['main-query']['use-cache']

		data = []

		if doNeedToUseCache:
			data = self.loadFromFile()
		else:
			data = self.handleMainQuery()

		self.mainData = {f[0]:f[1] for f in data}

	def getExistingItemsInWiki(self, wiki):
		fullSQL = SQL_EXISTING_ITEMS_TEMPLATE.format(wiki)
		filename = config['main-query']['filename-lang'].format(wiki)

		if os.path.isfile(filename):
			data = eval(open(filename,'r',encoding='utf-8').read())
			return data

		queryData = self.runQuery(fullSQL)

		finalData = []

		for row in queryData:
			finalData.append([encode_if_necessary(row[b]) for b in row])
		
		saveToFile(filename, json.dumps(finalData, ensure_ascii=False))

		return finalData

	def removeNotNeededItems(self):
		uniqueLangsInLangData = list(self.langData)

		for itemID in self.mainData:
			iws = self.mainData[itemID]
			
			for lang in uniqueLangsInLangData:
				if len(set([itemID]) & self.langData[lang]) == 0:
					if lang in self.langLists:
						self.langLists[lang].update({itemID: iws})
					else:
						self.langLists[lang] = {itemID: iws}

					self.goodItems.append(itemID)
		
	def handleWikidataDBLogic(self):
		self.getMainData()

		for lang in config['langs']:
			self.langData.update({lang: set(self.getExistingItemsInWiki(lang))})
		
		self.removeNotNeededItems()

if __name__ == '__main__':
	inst = Wikidata()
	inst.handleWikidataDBLogic()
	#inst.getExistingItemsInWiki('lv')