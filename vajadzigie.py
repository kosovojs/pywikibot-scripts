#!/usr/bin/python
# -*- coding: utf-8  -*-
import re, os
import json, requests
import pywikibot, operator
import toolforge
from pywikibot import xmlreader
from pywikibot import textlib
from bz2 import BZ2File
from collections import Counter
from checkDump import getLastFile, setLastDump

conn = toolforge.connect('lvwiki_p')
site = pywikibot.Site("lv", "wikipedia")

#xmlfile = 'ltgwiki-20160901-pages-articles.xml'
#paths = '/public/dumps/public/lvwiki/20180901/lvwiki-20180901-pages-articles.xml.bz2'

#os.chdir(r'projects/dumps')

def getLastFile1():
	return getLastFile()

def first_part(fileToParse):
	file = open("vajadzigie-raksti-lv-part1.txt", "w", encoding='utf-8')
	num = 0
	kopejaissaraksts = []
	regexpat = "\[\[([^\|\]#]+)"
	
	with BZ2File(fileToParse) as xml_file:
		for page in xmlreader.XmlDump(fileToParse).parse():
			if page.ns == "0" and not page.isredirect:
				num += 1
				if num % 1000 == 0:
					print(num)
				
				links = [match.group(1)[0].upper() + match.group(1)[1:] for match in re.finditer(regexpat,textlib.unescape(page.text)) if not re.search('^[a-z]{2,3}:',match.group(1))]
				links = [link.replace('_',' ') for link in links]
				links = list(set(links))
				
				kopejaissaraksts.extend(links)
			
	#pywikibot.output(kopejaissaraksts)
	#pywikibot.output(Counter(kopejaissaraksts))
	
	#file.write( str(Counter(kopejaissaraksts)))
	
	return Counter(kopejaissaraksts)
#
def run_query():
	#query = query.encode('utf-8')
	#print(query)
	SQL = """Select page_title from page where page_namespace=0"""
	try:
		cursor = conn.cursor()
		cursor.execute(SQL)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b
#
def get_quarry():
	
	
	lvwiki = run_query()
	file = [encode_if_necessary(b[0]).replace('_',' ') for b in lvwiki]
	
	return file
#

def second_part(data):
	file = data

	count1 = 0
	
	fsdfd = []
	
	badheads = re.compile('^:?(file|category|kategorija|attēls|wp):', re.I)

	print('here1fsdfsdsfsdfsdfsd')
	for value, count in file.most_common():
		if re.search(badheads,value):
			continue
		fsdfd.append(value)
	print('here1fsdfsdfdfsdf')

	print('here1')
	quarrydata = get_quarry()

	print('here2')
	itemlist = quarrydata#[item[0].replace('_',' ') for item in quarrydata]

	print('here3')
	dsfsdsd = list(set(fsdfd) - set(itemlist))

	print('here4')
	#pywikibot.output(dsfsdsd)

	file2 = open("vajadzigie-raksti-lv-part2.txt", "w", encoding='utf-8')
	file2.write(str(dsfsdsd))
	
	return dsfsdsd
#
mondict = {
	'1':'janvārī',
	'2':'februārī',
	'3':'martā',
	'4':'aprīlī',
	'5':'maijā',
	'6':'jūnijā',
	'7':'jūlijā',
	'8':'augustā',
	'9':'septembrī',
	'10':'oktobrī',
	'11':'novembrī',
	'12':'decembrī'
}

def makeDateReadable(inputstring):
	dateparts = re.search('(\d{4})(\d\d)(\d\d)',str(inputstring))
	year,mon,date = dateparts.group(1,2,3)
	mockedUp = "{}. gada {}. {}".format(year, date.lstrip('0'),mondict[mon.lstrip('0')])
	
	return mockedUp

def part_three(init,second,timestamp):
	file2 = open("links-lv-out2-red------0.txt", "w", encoding='utf-8')
	file21 = open("links-lv-out2-red------1.txt", "w", encoding='utf-8')
	fdgfg = init.most_common()
	
	readabledata = makeDateReadable(timestamp)

	fdfd = {}
	badheads = re.compile('^:?(file|category|image|kategorija|attēls|d):', re.I)
	for value, count in fdgfg:
		fdfd.update({value:count})

	outputsss = {}
	#count = 0

	print(len(second))

	for varsd in second:
		#if varsd in fdgfg:
		#	print('yes')
		#	continue
		#count = +1
		
		if '#' in varsd:
			continue
		
		#if count % 1000 == 0:
		#	print(count)
		something = fdfd[varsd]
		if something<10:
			continue
		#fsdf = '* [['+varsd+']] - '+str(something)
		outputsss.update({varsd:something})
		
		#try:
		#	something = fdgfg[varsd]
		#	fsdf = '* [['+varsd+']] - '+str(something)
		##	outputsss.append()
		#except KeyError:
		

	#outputsss = [value+'\t'+str(count) for value, count in file.most_common() if not re.search(badheads,value)]
	#outputsss = ['* [['+value+']] - '+str(count)  if value in itemlist2 and not re.search(badheads,value)]
	print(len(outputsss))

	sorted_x = sorted(outputsss.items(), key=operator.itemgetter(1), reverse=True)

	outputsssghfg = ['* [['+x+']] — '+str(y) for x, y in sorted_x if not re.search(badheads,x)]
	outputsssghfgsfsd = ['|[['+x+']]' for x, y in sorted_x if not re.search(badheads,x)]
	
	dsfsdf = """Šajā sarakstā parādās raksti, uz kuriem ir visvairāk vikisaišu Vikipēdijas rakstu vārdtelpas rakstu vikitekstā. Saraksts atjaunināts [https://dumps.wikimedia.org/lvwiki/{}/ {}].

__TOC__

== Saraksts ==
{{{{div col|3}}}}
""".format(timestamp,readabledata)

	endf = """
{{div col end}}

== Skatīt arī ==
* [[/Vecā versija|Saraksta vecā versija]]
* [[/Visas sarkanās saites|Visas sarkanās saites]]

[[Kategorija:Vikipēdija]]"""

	tofile =  '{{#invoke:list|horizontal|{{#invoke:random|list|limit=10|sep=dot\n' + "\n".join(outputsssghfgsfsd[:1000]) + """}}}}<noinclude>
{{dokumentācija}}

[[Kategorija:Vikipēdijas veidnes]]</noinclude>"""


	tofile2 = dsfsdf + "\n".join(outputsssghfg[:300000]) + endf

	file2.write(str(tofile))
	
	page = pywikibot.Page(site,"Vikipēdija:Vajadzīgie raksti")
	page.text = tofile2
	page.save(comment="Bots: atjaunināts", botflag=False, minor=False)
	
	file21.write(str(tofile2))
	
	page = pywikibot.Page(site,"Veidne:Vajadzīgie raksti")
	page.text = tofile
	page.save(comment="Bots: atjaunināts", botflag=False, minor=False)
#
def main():
	lastdata = getLastFile1()
	
	if not lastdata: return 0
	
	filelink = lastdata['path']
	dateStr = lastdata['date']
	
	initial = first_part(filelink)
	#initial = eval(open("vajadzigie-raksti-lv-part1.txt", "r", encoding='utf-8').read())
	from_seond = second_part(initial)
	part_three(initial,from_seond,dateStr)
	
	setLastDump(str(dateStr))
#
main()