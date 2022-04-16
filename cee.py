import pywikibot
import requests, logging
from pywikibot import textlib
from bs4 import BeautifulSoup, Tag
import re, mwparserfromhell, os, collections, os
from collections import OrderedDict

#os.chdir(r'projects/cee4')

DEBUG = False

logging.basicConfig(filename='cee-2022-stats.log', filemode='a+', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

topiclist = ['tēma','tēma2','tēma3']
countrylist = ['valsts','valsts2','valsts3']

pagecontTpl = """{{{{CEE Spring 2022 navigācija}}}}
== Konkursā iesniegtie raksti ==
{}

== Izveidotie raksti pēc autora ==
{}

== Izveidotie raksti pēc valsts/reģiona ==
{}

== Izveidotie raksti pēc tēmas ==
{}

[[Kategorija:CEE Spring 2022|Statistika]]
"""


latvian = [
	('ā','a'),
	('ē','e'),
	('ī','i'),
	('ū','u'),
	('Ā','A'),
	('Ē','E'),
	('Ī','I'),
	('Ū','U'),
	##
	('Č','Cz'),
	('Ģ','Gz'),
	('Ķ','Kz'),
	('Ļ','Lz'),
	('Ņ','Nz'),
	('Š','Sz'),
	('Ž','Zz')
]

def multisub(subs, subject):
	"Simultaneously perform all substitutions on the subject string."
	pattern = '|'.join('(%s)' % re.escape(p) for p, s in subs)
	#pywikibot.output(pattern)
	substs = [s for p, s in subs]
	#pywikibot.output(substs)
	replace = lambda m: substs[m.lastindex - 1]
	#pywikibot.output(replace)
	return re.sub(pattern, replace, subject)
#

def first_upper(stringo):
	if len(stringo)>0:

		return stringo[0].upper() + stringo[1:]
	else:
		return stringo

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def extractDisscussionData(pagetext):
	for template, fielddict in textlib.extract_templates_and_params(pagetext, remove_disabled_parts=False, strip=True):
		tplname = template.lower().strip().replace('_',' ')

		if tplname not in ['cee spring 2022']:
			continue

		fielditems = [[k[0],k[1]] for k in fielddict.items()]

		return fielditems

	return None

def getparam(tlobject,params):
	for param in params:

		if tlobject.has(param):
			val = tlobject.get(param).value.strip()

			if val!='':
				return val
				break

		#else:
	return False


maintable = """{{| class="sortable wikitable"
|-
{}
{}
|}}"""

topiclist = ['tēma','tēma2','tēma3']
countrylist = ['valsts','valsts2','valsts3']

class CEE:
	wiki = 'lv'
	pages = []#['Donbass', 'Basketbols 1980. gada vasaras olimpiskajās spēlēs']
	pageData = []
	proseSize = {}

	def getPagetitle(self, title):
		return title.replace('Diskusija:','')

	def getTalkpagetitle(self, title):
		return "Diskusija:{}".format(title)

	def getProseSize(self, htmlText):
		soup = BeautifulSoup(htmlText, "html.parser")

		for tag in soup.find_all('table'):
			tag.replaceWith('')

		for tag in soup.find_all('span',{'class':'noexcerpt'}):
			tag.replaceWith('')

		for tag in soup.find_all('span',{'class':'mw-editsection'}):
			tag.replaceWith('')

		for tag in soup.find_all('ol',{'class':'references'}):
			tag.replaceWith('')

		for tag in soup.find_all('h2'):
			tag.replaceWith('')

		for tag in soup.find_all('h3'):
			tag.replaceWith('')

		for tag in soup.find_all('h4'):
			tag.replaceWith('')

		thistext = str(soup.get_text()).strip('\s\n')
		thistext = thistext.replace('\n','')

		return len(thistext)

	def getTemplateContentBatch(self, titles):
		response = requests.get("https://{}.wikipedia.org/w/api.php".format(self.wiki), params={
			"action": "query",
			"format": "json",
			"prop": "revisions",
			"titles": '|'.join([self.getTalkpagetitle(f) for f in titles]),
			"rvprop": "content",
			"rvslots": "main",
			"rvdir": "older"
		})
		json_response = response.json()

		pageIDs = list(json_response['query']['pages'].keys())

		for pageID in pageIDs:
			pageData = json_response['query']['pages'][pageID]
			pageTitle = self.getPagetitle(pageData['title'])
			pageText = pageData['revisions'][0]['slots']['main']['*']

			templateData = extractDisscussionData(pageText)

			self.pageData.append([pageTitle, templateData])

	def getArticles(self):
		response = requests.get("https://{}.wikipedia.org/w/api.php".format(self.wiki), params={
			"action": "query",
			"format": "json",
			"prop": "transcludedin",
			"titles": "Veidne:CEE Spring 2022",
			"tiprop": "title|redirect",
			"tinamespace": "1",
			"tilimit": "max"
		})
		jsonResp = response.json()
		cnt = None

		responses = []
		responses.append(jsonResp)
		counter = 0

		while 'continue' in jsonResp:
			resp = requests.get("https://{}.wikipedia.org/w/api.php".format(self.wiki), params={
				"action": "query",
				"format": "json",
				"prop": "transcludedin",
				"titles": "Veidne:CEE Spring 2022",
				"tiprop": "title|redirect",
				"tinamespace": "1",
				#"tilimit": "25",
				"ticontinue": cnt
			})
			jsonResp = resp.json()
			if 'continue' in jsonResp:
				cnt = jsonResp['continue']['ticontinue']

			responses.append(jsonResp)

		allPages = []
		for rspns in responses:
			pageID = list(rspns['query']['pages'].keys())[0]

			pages = rspns['query']['pages'][pageID]['transcludedin'] if 'transcludedin' in rspns['query']['pages'][pageID] else []
			allPages.extend(pages)

		if DEBUG:
			self.pages = list(set([self.getPagetitle(f['title']) for f in allPages]))[:5]
		else:
			self.pages = list(set([self.getPagetitle(f['title']) for f in allPages]))

	def getTemplateContent(self):
		for batch in chunker(self.pages, 10):
			self.getTemplateContentBatch(batch)

	def articleProse(self, title):
		response = requests.get("https://{}.wikipedia.org/w/api.php".format(self.wiki), params={
			"action": "parse",
			"format": "json",
			"prop": "text",
			"page": title
		})

		json_response = response.json()

		htmlContent = json_response['parse']['text']['*']

		prose = self.getProseSize(htmlContent)

		self.proseSize.update({title: prose})



	def proseSizes(self):
		for page in self.pages:
			self.articleProse(page)

	def main(self):
		#print('started')
		self.getArticles()
		self.getTemplateContent()
		self.proseSizes()

		#print(self.proseSize)

class CEEStats:
	users = []
	topics = []
	countries = []

	articleData = []
	prosesize = {}

	def __init__(self, articleData, prosesize):
		self.prosesize = prosesize
		self.articleData = articleData

	def main_table(self, rawdata):
		bigdict = {}

		for article in self.articleData:
			title, data = article
			dict = {}
			for it in data:
				if it[1]!='':#izmantoti tukši parametri: ['tēma2', '']
					dict.update({it[0]:it[1]})

			bigdict.update({title:dict})

		head_conv = {
			'tēma':'1. tēma',
			'tēma2':'2. tēma',
			'tēma3':'3. tēma',
			'valsts':'1. valsts',
			'valsts2':'2. valsts',
			'valsts3':'3. valsts',
			'dalībnieks':'Dalībnieks'
		}

		cols = set()
		for d in bigdict.values():
			cols.update(d.keys())
		cols = list(sorted(cols))

		newheader = "! Raksts !! " + " !! ".join([head_conv[str(c)] for c in cols]) + " !! Lasāmā teksta garums !! Raksta garums baitos"

		datas = []

		for row, d_cols in sorted(bigdict.items(), key= lambda x: multisub(latvian, x[0])):
			e_cols = OrderedDict().fromkeys(cols)
			e_cols.update(d_cols)
			if row in self.prosesize:
				raksta_garums = self.prosesize[row]
			else:
				raksta_garums = '?'

			article_data_values = [first_upper(str(v).replace('None','')) for v in e_cols.values()]
			creatorart = article_data_values[0]
			realdata = article_data_values[1:]
			fsdfd = ' || '.join(realdata)

			thisrow = "|-\n| [[{}]] || {{{{U|{}}}}} || {} || {} || {{{{PAGESIZE:{}}}}}".format(row.replace('_',' '),creatorart,fsdfd,raksta_garums,row.replace('_',' '))

			datas.append(thisrow)

		maintable2 = maintable.format(newheader,'\n'.join(datas))

		return maintable2

	def make_table(self, pytlist,typoeconerter):
		fdfsd = collections.Counter(pytlist)

		counterobj = fdfsd.most_common()

		tabeltre = '{{| class="sortable wikitable"\n|-\n! {} !! Rakstu skaits\n'

		rows = []

		typecon = {
			'user':'{{{{U|{}}}}}',
			'country':'[[:Kategorija:CEE Spring 2022 raksti — {0}|{0}]]',
			'topic':'[[:Kategorija:CEE Spring 2022 raksti — {0}|{0}]]'
		}

		typecon2 = {
			'user':'Dalībnieks',
			'country':'Valsts/reģions',
			'topic':'Temats'
		}

		counterobj = sorted(counterobj, key= lambda x: (-x[1], multisub(latvian, x[0])))

		for name, count in counterobj:
			if typoeconerter == 'topic':
				name = name.lower()
			rows.append("|-\n| {} || {}".format(typecon[typoeconerter].format(name), count))

		tabeltoret = tabeltre.format(typecon2[typoeconerter]) + '\n'.join(rows) + '\n|}'

		return tabeltoret

	def main(self):
		if len(self.articleData) == 0:
			return

		for article in self.articleData:
			title, data = article
			dict = {}
			for it in data:
				if it[1]!='':
					dict.update({it[0]:it[1]})

			for itt in topiclist:
				if itt in dict:
					self.topics.append(first_upper(dict[itt]))

			for itt2 in countrylist:
				if itt2 in dict:
					self.countries.append(first_upper(dict[itt2]))

			if 'dalībnieks' in dict:
				self.users.append(first_upper(dict['dalībnieks']))

		#pywikibot.output(topics)
		#pywikibot.output(countries)
		#pywikibot.output(users)

		topict = self.make_table(self.topics,'topic')
		countrtable = self.make_table(self.countries,'country')
		usertable = self.make_table(self.users,'user')

		#todo: Kopā konkursam iesniegti X raksti.

		pagecont2 = pagecontTpl.format(self.main_table(self.articleData),usertable,countrtable,topict)
		#[[Attēls:CEES2018.svg|thumb|350px|Izveidotie raksti pēc dienas]]

		if DEBUG:
			with open('cee_test','w', encoding='utf-8') as fileSave:
				fileSave.write(pagecont2)
		else:
			site = pywikibot.Site("lv", "wikipedia")
			articletitle = 'Vikipēdija:CEE Spring 2022/Statistika'
			saglapa = pywikibot.Page(site,articletitle)

			saglapa.text = pagecont2

			saglapa.save(summary='bots: atjaunināts (kopējais rakstu skaits: {})'.format(len(self.articleData)), botflag=False, minor=False)

logging.info('Process start')
inst = CEE()
inst.main()

logging.info('Ended stats gathering, pages in total: {}'.format(len(inst.pageData)))

statsInst = CEEStats(inst.pageData, inst.proseSize)
statsInst.main()
logging.info('Process end')
