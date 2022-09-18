import bz2, re
import json, os
from time import time
import logging

titlesToCheck = json.loads(open('sites_data.json', 'r', encoding='utf-8').read())
titlesToCheck = tuple([f[1] for f in titlesToCheck])

logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

MAX_ITEM = 500

def get_dump_lines(path):
	mode = 'r'
	file_ = os.path.split(path)[-1]
	if file_.endswith('.bz2'):
		f = bz2.BZ2File(path, mode)
	elif file_.endswith('.json'):
		f = open(path, mode)
	else:
		raise NotImplementedError('Reading file is not supported')
	try:
		for line in f:
			if isinstance(line, bytes):
				line = line.decode('utf-8')
			try:
				yield json.loads(line.strip().strip(','))
			except json.JSONDecodeError:
				continue
	finally:
		f.close()

class WikidataDumpParser:
	labelStatements = []
	coordinatesStatements = []
	propertyStatements = []
	statsStatements = []
	qualities = {}

	currItem = None
	#file_json = json.loads(open('dfsdfsd.json','r',encoding='utf-8').read())
	d = 0
	counter = 0

	redis_conn = None

	def getFile(self):
		with bz2.open('/mnt/nfs/dumps-labstore1007.wikimedia.org/other/wikibase/wikidatawiki/20220411/wikidata-20220411-all.json.bz2', mode='rt') as f:
			f.read(2) # skip first two bytes: "{\n"
			for line in f:
				try:
					yield json.loads(line.rstrip(',\n'))
				except json.decoder.JSONDecodeError:
					continue

	def main(self):
		logging.info('STARTED PROCESS')
		fileObj = get_dump_lines('/mnt/nfs/dumps-labstore1007.wikimedia.org/other/wikibase/wikidatawiki/20220411/wikidata-20220411-all.json.bz2')

		for_save = []

		for record in fileObj:
			self.counter += 1

			self.currItem = record['id']

			claims = record.get('claims')

			if claims: continue

			sitelinks = record.get('sitelinks')

			#print(sitelinks)
			#{'arwiki': {'site': 'arwiki', 'badges': [], 'title': 'سعد جابر (توضيح)'}}
			for wiki in sitelinks:
				if wiki != 'commonswiki':
					title = sitelinks.get(wiki).get('title', '')
					if ':' in title and title.startswith(titlesToCheck):
						for_save.append(json.dumps([self.currItem, wiki, title]))
						#break

			if len(for_save) > 500:
				with open('to_save.txt', 'a', encoding='utf-8') as file_w:
					file_w.write("{}\n".format('\n'.join(for_save)))
					for_save = []

			if self.counter % 10000 == 0:
				logging.info("logging: {} - {} - {}".format(self.d, self.counter, self.currItem))

		with open('to_save2.txt', 'a', encoding='utf-8') as file_w:
			file_w.write("{}\n".format('\n'.join(for_save)))
			for_save = []

		print('finished process')
		logging.info('FINISHED PROCESS')
		#return self.labelStatements
		#print(self.labelStatements)
#
parser = WikidataDumpParser()
parser.main()
logging.info('-'*100)
