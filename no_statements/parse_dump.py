import bz2, re
import json, os
from time import time
import logging

titlesToCheck = json.loads(open('sites_data.json', 'r', encoding='utf-8').read())
titlesToCheck = tuple([f[1] for f in titlesToCheck])

logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

MAX_ITEM = 500

wplist = set(['abwiki', 'acewiki', 'adywiki', 'afwiki', 'akwiki', 'amwiki', 'anwiki', 'angwiki', 'arwiki', 'arcwiki', 'arzwiki', 'aswiki', 'astwiki', 'atjwiki', 'avwiki', 'aywiki', 'azwiki', 'azbwiki', 'bawiki', 'barwiki', 'bclwiki', 'bewiki', 'be_x_oldwiki', 'bgwiki', 'bhwiki', 'biwiki', 'bjnwiki', 'bmwiki', 'bnwiki', 'bowiki', 'bpywiki', 'brwiki', 'bswiki', 'bugwiki', 'bxrwiki', 'cawiki', 'cbk_zamwiki', 'cdowiki', 'cewiki', 'cebwiki', 'chwiki', 'chrwiki', 'chywiki', 'ckbwiki', 'cowiki', 'crwiki', 'crhwiki', 'cswiki', 'csbwiki', 'cuwiki', 'cvwiki', 'cywiki', 'dawiki', 'dewiki', 'dinwiki', 'diqwiki', 'dsbwiki', 'dtywiki', 'dvwiki', 'dzwiki', 'eewiki', 'elwiki', 'emlwiki', 'test2wiki', 'enwiki', 'testwiki', 'simplewiki', 'eowiki', 'eswiki', 'etwiki', 'euwiki', 'extwiki', 'fawiki', 'ffwiki', 'fiwiki', 'fjwiki', 'fowiki', 'frwiki', 'frpwiki', 'frrwiki', 'furwiki', 'fywiki', 'gawiki', 'gagwiki', 'ganwiki', 'gdwiki', 'glwiki', 'glkwiki', 'gnwiki', 'gomwiki', 'gotwiki', 'alswiki', 'guwiki', 'gvwiki', 'hawiki', 'hakwiki', 'hawwiki', 'hewiki', 'hiwiki', 'hifwiki', 'hrwiki', 'hsbwiki', 'htwiki', 'huwiki', 'hywiki', 'iawiki', 'idwiki', 'iewiki', 'igwiki', 'ikwiki', 'ilowiki', 'iowiki', 'iswiki', 'itwiki', 'iuwiki', 'jawiki', 'jamwiki', 'jbowiki', 'jvwiki', 'kawiki', 'kaawiki', 'kabwiki', 'kbdwiki', 'kbpwiki', 'kgwiki', 'kiwiki', 'kkwiki', 'klwiki', 'kmwiki', 'knwiki', 'kowiki', 'koiwiki', 'krcwiki', 'kswiki', 'kshwiki', 'kuwiki', 'kvwiki', 'kwwiki', 'kywiki', 'lawiki', 'ladwiki', 'lbwiki', 'lbewiki', 'lezwiki', 'lgwiki', 'liwiki', 'lijwiki', 'lmowiki', 'lnwiki', 'lowiki', 'lrcwiki', 'ltwiki', 'ltgwiki', 'lvwiki', 'zh_classicalwiki', 'maiwiki', 'map_bmswiki', 'mdfwiki', 'mgwiki', 'mhrwiki', 'miwiki', 'minwiki', 'mkwiki', 'mlwiki', 'mnwiki', 'mrwiki', 'mrjwiki', 'mswiki', 'mtwiki', 'mwlwiki', 'mywiki', 'myvwiki', 'mznwiki', 'nawiki', 'nahwiki', 'zh_min_nanwiki', 'napwiki', 'nowiki', 'ndswiki', 'nds_nlwiki', 'newiki', 'newwiki', 'nlwiki', 'nnwiki', 'novwiki', 'nrmwiki', 'nsowiki', 'nvwiki', 'nywiki', 'ocwiki', 'olowiki', 'omwiki', 'orwiki', 'oswiki', 'pawiki', 'pagwiki', 'pamwiki', 'papwiki', 'pcdwiki', 'pdcwiki', 'pflwiki', 'piwiki', 'pihwiki', 'plwiki', 'pmswiki', 'pnbwiki', 'pntwiki', 'pswiki', 'ptwiki', 'quwiki', 'rmwiki', 'rmywiki', 'rnwiki', 'rowiki', 'roa_tarawiki', 'ruwiki', 'ruewiki', 'roa_rupwiki', 'rwwiki', 'sawiki', 'sahwiki', 'scwiki', 'scnwiki', 'scowiki', 'sdwiki', 'sewiki', 'sgwiki', 'bat_smgwiki', 'shwiki', 'siwiki', 'skwiki', 'slwiki', 'smwiki', 'snwiki', 'sowiki', 'sqwiki', 'srwiki', 'srnwiki', 'sswiki', 'stwiki', 'stqwiki', 'suwiki', 'svwiki', 'swwiki', 'szlwiki', 'tawiki', 'tcywiki', 'tewiki', 'tetwiki', 'tgwiki', 'thwiki', 'tiwiki', 'tkwiki', 'tlwiki', 'tnwiki', 'towiki', 'tpiwiki', 'trwiki', 'tswiki', 'ttwiki', 'tumwiki', 'twwiki', 'tywiki', 'tyvwiki', 'udmwiki', 'ugwiki', 'ukwiki', 'urwiki', 'uzwiki', 'vewiki', 'vecwiki', 'vepwiki', 'viwiki', 'vlswiki', 'vowiki', 'fiu_vrowiki', 'wawiki', 'warwiki', 'wowiki', 'wuuwiki', 'xalwiki', 'xhwiki', 'xmfwiki', 'yiwiki', 'yowiki', 'zh_yuewiki', 'zawiki', 'zeawiki', 'zhwiki', 'zuwiki'])

DATE = '20230102'

def get_best_claim_ids(prop_data):
	ids = {'normal': [], 'best': []}
	for claim in prop_data:
		rank = claim.get('rank', '')

		if rank == 'normal':
			ids['normal'].append(claim.get('id'))

		if rank == 'preferred':
			ids['best'].append(claim.get('id'))

	if len(ids['best']) > 0:
		return ids['best']

	return ids['normal']

def get_best_claim(prop_data):
	best_ids = get_best_claim_ids(prop_data)
	values = []

	for claim in prop_data:
		if claim.get('id', '') not in best_ids: continue

		datatype = claim['mainsnak']['datatype']

		claimtosave = None

		if 'datavalue' in claim['mainsnak']:
			if datatype in ('external-id','string','commonsMedia','url'):
				claimtosave = claim['mainsnak']['datavalue']['value']
			elif datatype=='wikibase-item':
				claimtosave = claim['mainsnak']['datavalue']['value']['id']
			elif datatype=='time':
				claimtosave = claim['mainsnak']['datavalue']['value']['time']+'/'+str(claim['mainsnak']['datavalue']['value']['precision'])
			elif datatype=='quantity':
				claimtosave = claim['mainsnak']['datavalue']['value']['amount']+'U'+str(claim['mainsnak']['datavalue']['value']['unit'].replace('http://www.wikidata.org/entity/Q',''))
			elif datatype=='monolingualtext':
				claimtosave = claim['mainsnak']['datavalue']['value']['language']+': '+claim['mainsnak']['datavalue']['value']['text']
			elif datatype=='globe-coordinate':
				val = claim['mainsnak']['datavalue']['value']
				claimtosave = val['latitude']+','+val['longitude']+','+val['precision']
			else:
				#print(prop, datatype)
				pass

			values.append(claimtosave)

	return values

FILE_PATH = '/public/dumps/public/other/wikibase/wikidatawiki/{}/wikidata-{}-all.json.bz2'.format(DATE, DATE)

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
	currItem = None
	#file_json = json.loads(open('dfsdfsd.json','r',encoding='utf-8').read())
	d = 0
	counter = 0
	record = None

	to_add_p31_mnt_pages = []
	women_entries = []
	coordinates = []

	redis_conn = None

	def check_women_pages(self):
		claims = self.record.get('claims')
		if claims: return

		sitelinks = self.record.get('sitelinks')

		instance_of = get_best_claim(claims.get('P31', {}))
		if 'Q5' not in instance_of: return

		gender = get_best_claim(claims.get('P21', {}))
		if 'Q6581072' not in gender: return

		iwcount = len(set(sitelinks.keys())&wplist)

		if iwcount < 1: return

		self.women_entries.append("{}\t{}".format(self.currItem, iwcount))

	def check_coordinates(self):
		claims = self.record.get('claims')
		if claims: return

		coords = get_best_claim(claims.get('P625', {}))
		if len(coords) == 0: return

		countries = get_best_claim(claims.get('P17', {}))

		self.coordinates.append(json.dumps(self.currItem, coords, countries))

	def check_p31_mnt_pages(self):
		claims = self.record.get('claims')

		if claims: return

		sitelinks = self.record.get('sitelinks')

		#print(sitelinks)
		#{'arwiki': {'site': 'arwiki', 'badges': [], 'title': 'سعد جابر (توضيح)'}}
		for wiki in sitelinks:
			if wiki != 'commonswiki':
				title = sitelinks.get(wiki).get('title', '')
				if ':' in title and title.startswith(titlesToCheck):
					self.to_add_p31_mnt_pages.append(json.dumps([self.currItem, wiki, title]))

	def save_status(self, force = False):
		if force or len(self.to_add_p31_mnt_pages) > 500:
			with open('./logs/to_add_p31_mnt_pages.txt', 'a', encoding='utf-8') as file_w:
				file_w.write("{}\n".format('\n'.join(self.to_add_p31_mnt_pages)))
				self.to_add_p31_mnt_pages = []

		if force or len(self.coordinates) > 500:
			with open('./logs/coordinates.txt', 'a', encoding='utf-8') as file_w:
				file_w.write("{}\n".format('\n'.join(self.coordinates)))
				self.coordinates = []

		if force or len(self.women_entries) > 500:
			with open('./logs/women_entries.txt', 'a', encoding='utf-8') as file_w:
				file_w.write("{}\n".format('\n'.join(self.women_entries)))
				self.women_entries = []

	def getFile(self):
		with bz2.open(FILE_PATH, mode='rt') as f:
			f.read(2) # skip first two bytes: "{\n"
			for line in f:
				try:
					yield json.loads(line.rstrip(',\n'))
				except json.decoder.JSONDecodeError:
					continue

	def main(self):
		logging.info('STARTED PROCESS')
		fileObj = get_dump_lines(FILE_PATH)

		for record in fileObj:
			self.counter += 1

			self.currItem = record['id']

			self.record = record

			self.check_p31_mnt_pages()
			self.check_women_pages()
			self.check_coordinates()

			self.save_status()

			if self.counter % 10000 == 0:
				logging.info("logging: {} - {} - {}".format(self.d, self.counter, self.currItem))
				#break

		self.save_status(True)

		print('finished process')
		logging.info('FINISHED PROCESS')
		#return self.labelStatements
		#print(self.labelStatements)
#
parser = WikidataDumpParser()
parser.main()
logging.info('-'*100)
