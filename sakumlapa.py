#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from datetime import date, datetime, timedelta
import pywikibot
import json
from collections import Counter
import operator

botflag = False

site = pywikibot.Site("lv", "wikipedia")

#day1 = open("18dat.json", "r", encoding='utf-8').read()
#day2 = open("17dat.json", "r", encoding='utf-8').read()

configuration = pywikibot.Page(site,'Dalībnieks:Edgars2007/Skatītākie raksti/configuration.json')
configuration = configuration.get()
configuration = eval(configuration)

#configuration = {"config":{"articlecount":10,"exclude":['Sākumlapa','Latvija']}}

#data1 = json.loads(day1)
#data2 = json.loads(day2)

#[data1,data2]

#https://wikimedia.org/api/rest_v1/metrics/pageviews/top/lv.wikipedia.org/all-access/2016/08/02

def getdata():
	files = []
	fisrtday = datetime.now()#datetime(2013, 3, 11)
	
	daycounttoinclude = int(configuration['config']['daycount'])

	for daySUB in range(daycounttoinclude):
		daytoprint = (fisrtday - timedelta(days=1) - timedelta(days=daySUB)).date()
		day = daytoprint.strftime("%Y/%m/%d")
		urltoopen = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/lv.wikipedia.org/all-access/'+day
		res = requests.get(urltoopen).json()
		files.append(res)
		
		#print(now)
		
	return files

def datesToSub():
	files2 = []
	fisrtday = datetime.now()#datetime(2013, 3, 11)

	for daySUB in range(7):
		daytoprint = (fisrtday - timedelta(days=1) - timedelta(days=daySUB)).date()
		day = daytoprint.strftime("%d.%m")
		files2.append(day)
		
		#print(now)
		
	return files2[::-1]

articleFILES = getdata()

#conf = json.load(configuration)
#pywikibot.output(configuration['config']['articlecount'])
#pywikibot.output(configuration['config']['exclude'])


day1art = []

newdict = {}

for file in articleFILES:
	dict1 = {article1['article']: article1['views'] for article1 in file['items'][0]['articles']}
	#day1art.append(dict1)
	newdict = dict(Counter(dict1)+Counter(newdict))
	

"""
dict1 = {article1['article']: article1['views'] for article1 in data1['items'][0]['articles']}
dict2 = {article2['article']: article2['views'] for article2 in data2['items'][0]['articles']}

for article1 in data1['items'][0]['articles']:
	#pywikibot.output(article1)
	article = article1['article']
	views = article1['views']
	#pywikibot.output(article)
	#pywikibot.output(views)
	dict1.update({article:views})
	
for article2 in data2['items'][0]['articles']:
	#pywikibot.output(article1)
	article = article2['article']
	views = article2['views']
	#pywikibot.output(article)
	#pywikibot.output(views)
	dict2.update({article:views})
	
newdict = dict(Counter(dict1)+Counter(dict2))
"""
#http://stackoverflow.com/questions/11290092/python-elegantly-merge-dictionaries-with-sum-of-values
#http://stackoverflow.com/questions/10461531/merge-and-sum-of-two-dictionaries


sorted_x = sorted(newdict.items(), key=operator.itemgetter(1), reverse=True)#pēc tam sakārtot alfabēta sercībā

badtitles = ['Portāls:', 'Portāls:', 'Attēls:', 'File:', 'Veidnes diskusija:', 'Template talk:', 'Modulis:', 'Module:', 'Gadget:', 'Gadget:', 'MediaWiki:', 'MediaWiki:', 'Media:', 'Media:', 'Portāla diskusija:', 'Portāla diskusija:', 'Gadget talk:', 'Gadget talk:', 'Education Program talk:', 'Education Program talk:', 'Attēla diskusija:', 'File talk:', 'Palīdzība:', 'Help:', 'Education Program:', 'Education Program:', 'MediaWiki diskusija:', 'MediaWiki talk:', 'Gadget definition:', 'Gadget definition:', 'Special:', 'Special:', 'Vikipēdija:', 'Project:', 'Vikiprojekta diskusija:', 'Vikiprojekta diskusija:', 'Vikiprojekts:', 'Vikiprojekts:', 'Moduļa diskusija:', 'Module talk:', 'Veidne:', 'Template:', 'Dalībnieks:', 'User:', 'Diskusija:', 'Talk:', 'Kategorija:', 'Category:', 'Kategorijas diskusija:', 'Category talk:', 'Dalībnieka diskusija:', 'User talk:', 'Tēma:', 'Topic:', 'Gadget definition talk:', 'Gadget definition talk:', 'Vikipēdijas diskusija:', 'Project talk:', 'Palīdzības diskusija:', 'Help talk:', 'Dalībniece:', 'Lietotājs:', 'Dalībnieces diskusija:', 'Lietotāja diskusija:', 'VP:', 'WP:', 'Wikipedia:', 'Image:', 'Image talk:']#['Special:','Vikipēdija:','Palīdzība:','Vikiprojekts:','Kategorija:','Attēls:']
excluding = configuration['config']['exclude']#['Sākumlapa']
#excluding = excluding.append('xxs')

def checkbeforeadd(value):
	page = pywikibot.Page(site,value)
	
	if page.exists() and not (page.isRedirectPage() or page.isDisambig()):
		return True
	else:
		return False
	

def checkarticle(page):
	results1 = [title for title in badtitles if title in page]
	results2 = [title for title in excluding if title==page]
	
	if len(results1)==0 and len(results2)==0:
		return True
	else:
		return False

usingdata = [[f[0],f[1]] for f in sorted_x[:100] if checkarticle(f[0])]

#for dddd in usingdata:
#	pywikibot.output(dddd[0])
#	pywikibot.output(dddd[1])


pywikibot.output(usingdata)
articlesCONF = configuration['config']['articlecount']
articlesToadd = articlesCONF

count = 0

toMain = []

while count<articlesToadd:
	
	artic = usingdata[count][0]
	#if checkbeforeadd(artic):
	pywikibot.output(artic)
	count +=1
	toMain.append(artic.replace('_',' '))


def createSummarytable(data):
	outputtext = '{|class="sortable wikitable"\n|-\n! Lapa !! Skatījumi\n|-\n'
	
	for dddd in data:
		outputtext = outputtext + "|-\n| [[%s]] || %d\n" % (dddd[0].replace('_',' '),dddd[1])
		
	outputtext = outputtext + "|}"
	
	addeddates = datesToSub()
	
	outputtext = 'Iekļautie datumi: '+', '.join(addeddates)+'.\n\n'+outputtext
	
	report_pageE = pywikibot.Page(site,'Veidne:Skatītākie raksti Vikipēdijā/Statistika')
	report_pageE.text = outputtext
	report_pageE.save(summary='bots: atjaunināts', botflag=botflag, minor=False, as_group='sysop')

pagetosave = pywikibot.Page(site,'Veidne:Skatītākie raksti Vikipēdijā')

description2 = "]]|\n[[".join(toMain)

#arr3 = "]]\n* [[".join(toMain)


description = "{{hlist|Pagājušajā nedēļā skatītākais:<br />[[" + description2 + "]]}}<noinclude>\n{{dokumentācija}}</noinclude>"

pagetosave.text = description
pagetosave.save(summary='bots: atjaunināts', botflag=botflag, minor=False, as_group='sysop')

createSummarytable(usingdata)