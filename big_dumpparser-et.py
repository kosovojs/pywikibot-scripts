#!/usr/bin/python
# -*- coding: utf-8  -*-
import re, os, sys
import json, requests
import pywikibot, operator
import toolforge
from pywikibot import xmlreader
from pywikibot import textlib
from bz2 import BZ2File
from collections import Counter
from checkDump import getLastFile, setLastDump

conn = toolforge.connect('etwiki_p')
site = pywikibot.Site("et", "wikipedia")

xmlfile = '../../lvwiki-20180501-pages-articles.xml'
curdate = '2018-05-01'

#nākošais
check_nakosais = re.compile(r"(<\s*nowiki\s*\/\s*>)", flags=re.I)
file_nakosais = ''#open(r"lv-dumpscan-nakos.txt", "w", encoding='utf-8')
mas_nakosais = []
title_nakosais = 'User:Edgars2007/nowiki'
#isbn
check_isbn = re.compile(r"(?<![\|{])\s*isbn(?!\s*=)", flags=re.I)
file_isbn = ''#open(r"reps/lv-dumpscan-isbn-"+curdate+".txt", "w", encoding='utf-8')
mas_isbn = []
title_isbn = 'Dalībnieks:Edgars2007/ISBN/Plain'
#dubes - dubulti vārdi
#fixme: biotakso rakstus ignorēt
check_dubes = re.compile(r"\s(([A-Za-zĀČĒĢĪĶĻŅŠŪŽāčēģīķļņšūž]{3,})\s+\2)\s", flags=re.I)
file_dubes = ''#open(r"reps/lv-dumpscan-dubes-"+curdate+".txt", "w", encoding='utf-8')
mas_dubes = []
title_dubes = 'Dalībnieks:Edgars2007/Aka/Divi vienādi vārdi pēc kārtas'
#sekojoš
check_sekoj = re.compile(r"(sekojoš)", flags=re.I)
file_sekoj = ''#open(r"reps/lv-dumpscan-sekoj-"+curdate+".txt", "w", encoding='utf-8')
mas_sekoj = []
title_sekoj = 'Dalībnieks:Edgars2007/Aka/Typo/Sekojošais'

#years
check_years = re.compile(r"(\[\[.*?(\d{4}).*?\|(?!\2)\d{4}\]\])", flags=re.I)
file_years = ''#open(r"reps/lv-dumpscan-years-"+curdate+".txt", "w", encoding='utf-8')
mas_years = []
title_years = 'Dalībnieks:Edgars2007/Aka/Gadu saites'#nevajag kontekstu



def getLastFile1():

	return getLastFile(jobname='dumpsOther')

def parse_findings(regex,pagetext,pagetitle,file,data):
	m = regex.finditer(pagetext)
	context = 30
	finds = []
	if m:
		for found in m:
			sectionname = '<nowiki>'+pagetext[max(0, found.start() - context):found.start()]+'</nowiki><span style="background-color:#fdd;padding:2px;margin:1px">\'\'\''+pagetext[found.start():found.end()]+'\'\'\'</span><nowiki>'+pagetext[found.end() : found.end() + context] + '</nowiki>'
			sectionname = sectionname.replace('\n',' ')
			sectionname = re.sub('\s\s*',' ',sectionname)
			finds.append(sectionname)

		if len(finds)>0:
			#file.write('* [['+pagetitle+']]: '+', '.join(finds)+'\n')
			data.append([pagetitle,', '.join(finds)])

#
def parseFile(fileToParse):
	num = 0
	with BZ2File(fileToParse) as xml_file:
		for page in xmlreader.XmlDump(fileToParse).parse():
			if page.ns == "0" and not page.isredirect:
				num += 1
				if num % 2500 == 0:
					print(num)

				pagetext = textlib.unescape(page.text)
				pagetitle = page.title

				#nākošais
				parse_findings(check_nakosais,pagetext,pagetitle,file_nakosais,mas_nakosais)
				#isbn
				#parse_findings(check_isbn,pagetext,pagetitle,file_isbn,mas_isbn)
				#dubes
				#parse_findings(check_dubes,pagetext,pagetitle,file_dubes,mas_dubes)
				#sekojos
				#parse_findings(check_sekoj,pagetext,pagetitle,file_sekoj,mas_sekoj)
				#years
				#parse_findings(check_years,pagetext,pagetitle,file_years,mas_years)
#
def putWiki():
	for one in [(mas_nakosais,title_nakosais)]:
		mas,title = one

		file_nakosais = open(r"lv-dumpscan-nakos.txt", "w", encoding='utf-8')
		file_nakosais.write(str(mas))

		if len(mas)>0:
			thetext = ["* [[{}]]: {}".format(f[0],f[1]) for f in mas]
			page = pywikibot.Page(site,title)
			page.text = '\n'.join(thetext)
			page.save(comment="upd", botflag=False, minor=False)
#
def main():
	#lastdata = getLastFile1()
	#if not lastdata: return 0

	filelink = '/public/dumps/public/etwiki/20210401/etwiki-20210401-pages-articles.xml.bz2'
	dateStr = '20210401'#lastdata['date']

	parseFile(filelink)
	putWiki()

	#setLastDump(str(dateStr),'dumpsOther')

#
main()
