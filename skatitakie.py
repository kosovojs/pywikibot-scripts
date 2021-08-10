import requests
import traceback
from datetime import date, datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import urllib
import pywikibot
from pywikibot import pagegenerators
import json
from customFuncs import basic_petscan

botflag = False

headers = {
	'User-Agent': 'w:lv:User:Edgars2007/Missing popular2'.encode('utf8')
}

page_to_save = 'Veidne:Aktuāls notikums sākumlapā/Skatītākie raksti'

#file1323 = open("viewdata2.txt", "w", encoding='utf-8')


site = pywikibot.Site("lv", "wikipedia")


#pywikibot.config.family = "wikipedia"
#pywikibot.config.mylang = "en"
#usernames['wikipedia']['lv'] = 'EdgarsBot'
#pywikibot.config2.usernames['wikipedia']['lv'] = 'Edgars2007'
#site = pywikibot.Site()
#site.login()

pagetosave = pywikibot.Page(site,'Veidne:Aktuāls notikums sākumlapā/Skatītākie raksti')

#category = pywikibot.Category(site, u'Kategorija:2018. gada ziemas olimpiskās spēles')
#gen = pagegenerators.CategorizedPageGenerator(category, namespaces=0, recurse=2)

listarticles = basic_petscan('19656819')
catpages = [f['title'] for f in listarticles]

#file = open("views.json", "r", encoding='utf-8')

#file = file.read()

#json_data = json.loads(file)
#pywikibot.output(json_data['items'])
#'''

'''
catpages = []
for page23 in gen:
	article23 = page23.title()
	article23 = article23.replace(' ','_')
	catpages.append(article23)
'''
exclude = [

]

searchstr = "FIFA_Pas"
searchstr2 = "futbola"

count = 0
arr = []
arr2 = []


endpoints = {
	'article': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article',
	'project': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate',
	'top': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top',
}

#https://tools.wmflabs.org/topviews/#project=lv.wikipedia.org&platform=all-access&range=last-week&excludes=
#https://wikimedia.org/api/rest_v1/metrics/pageviews/top/lv.wikipedia.org/all-access/2016/08/02

project='lv.wikipedia.org'
access='all-access'
year=None
month=None
day=None
limit=1000

#get data
yesterday = date.today() - timedelta(days=1)
year = str(year or yesterday.year)
month = str(month or yesterday.month).rjust(2, '0')
day = str(day or yesterday.day).rjust(2, '0')

url = '/'.join([endpoints['top'], project, access, year, month, day])

result = requests.get(url, headers=headers).json()


for item in result['items'][0]['articles']:
	if count>7:
		break
	else:
		value = str(item['article'])
		if (searchstr in value or searchstr2 in value or value in catpages) and value not in exclude and 'Vikiprojekts:' not in value:
			#pywikibot.output("Found 'is' in the string.")



			page = pywikibot.Page(site,value)

			if page.exists() and not (page.isRedirectPage() or page.isDisambig()):
				pywikibot.output(value)
				value = value.replace("_"," ")
				arr.append(value)
				count = count+1

#get data end


description2 = "]]''|\n''[[".join(arr)

for itemarticle in exclude:
	itemarticle = itemarticle.replace("_"," ")
	#if itemarticle.startswith('Vikiprojekts:','Kategorija:'): continue
	#if 'Vikiprojekts:' in itemarticle
	arr2.append(itemarticle)

arr3 = "]]\n* [[".join(arr2)

''' No liekamajiem rakstiem tiek ignorēti šie izvēlētie raksti:
* [[%s]]
}}
'''
text = '''<noinclude>{{dokumentācija|content=Saraksts tiek atjaunināts no [%s šiem datiem].
}}
[[Kategorija:Vikipēdijas veidnes]]</noinclude>
''' % (url)

description = "{{hlist|''Vakardien skatītākais'': ''[[" + description2 + "]]''}}" + text

pywikibot.output(description)
#file1323.write(str(description))



pagetosave = pywikibot.Page(site,page_to_save)

pagetosave.text = description
pagetosave.save(summary='bots: atjaunināts', botflag=botflag, minor=False)#, as_group='sysop'
