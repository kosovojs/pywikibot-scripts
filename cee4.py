import pywikibot, re
import collections, os
from collections import OrderedDict

#os.chdir(r'projects/cee')

fileeopen = eval(open('cee-all-articles.txt','r', encoding='utf-8').read())

prosesize = eval(open('ceeraksti-prose22.txt','r', encoding='utf-8').read())
#['Velimirs_Kalandadze', [['dalībnieks', 'Ludis21345'], ['tēma', 'Sports'], ['valsts', 'Gruzija']]]

users = []
topics = []
countries = []

maintable = """{{| class="sortable wikitable"
|-
{}
{}
|}}"""

def main_table(rawdata):
	bigdict = {}
	
	for article in fileeopen:
		title, data = article
		dict = {}
		for it in data:
			#if it[0] in dict:
			#	pywikibot.output(article)
			if it[1]!='':#izmantoti tukši parametri: ['tēma2', '']
				dict.update({it[0]:it[1]})
			
		bigdict.update({title:dict})
#
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
#print("\t", "\t".join([str(c) for c in cols]))
#header = "\t"+"\t".join([str(c) for c in cols])
	newheader = "! Raksts !! " + " !! ".join([head_conv[str(c)] for c in cols]) + " !! Lasāmā teksta garums !! Raksta garums baitos"
	#pywikibot.output(newheader)
#pywikibot.output(cols)
#print(sorted(dict.items()))

	datas = []
#cols = [100, 200, 300]
# data rows
	
	#main_table_what_order = 
	
	for row, d_cols in sorted(bigdict.items()):
		e_cols = OrderedDict().fromkeys(cols)
		e_cols.update(d_cols)
		if row in prosesize:
			raksta_garums = prosesize[row]
		else:
			raksta_garums = '?'
	#print(row, "\t", "\t".join([str(v) for v in e_cols.values()]))
	#datarow = "{{P|"+row+"}}\t"+"\t".join([first_upper(str(v).replace('None','')) for v in e_cols.values()])
		article_data_values = [first_upper(str(v).replace('None','')) for v in e_cols.values()]
		creatorart = article_data_values[0]
		realdata = article_data_values[1:]
		fsdfd = ' || '.join(realdata)
	
		thisrow = "|-\n| [[{}]] || {{{{U|{}}}}} || {} || {} || {{{{PAGESIZE:{}}}}}".format(row.replace('_',' '),creatorart,fsdfd,raksta_garums,row.replace('_',' '))
	
	
	#pywikibot.output(article_data_values)
	
		datas.append(thisrow)
		
		
	maintable2 = maintable.format(newheader,'\n'.join(datas))
	
	return maintable2
#

def make_table(pytlist,typoeconerter):
	fdfsd = collections.Counter(pytlist)
	
	counterobj = fdfsd.most_common()
	#pywikibot.output(counterobj)
	
	tabeltre = '{{| class="sortable wikitable"\n|-\n! {} !! Rakstu skaits\n'
	
	rows = []
	
	typecon = {
		'user':'{{{{U|{}}}}}',
		'country':'[[{}]]',
		'topic':'{}'
	}
	
	typecon2 = {
		'user':'Dalībnieks',
		'country':'Valsts/reģions',
		'topic':'Temats'
	}
	
	for letter, count in counterobj:
		rows.append("|-\n| {} || {}".format(typecon[typoeconerter].format(letter), count))
	
	tabeltoret = tabeltre.format(typecon2[typoeconerter]) + '\n'.join(rows) + '\n|}'
	
	#pywikibot.output(tabeltoret)
	
	return tabeltoret

topiclist = ['tēma','tēma2','tēma3']
countrylist = ['valsts','valsts2','valsts3']

def first_upper(stringo):
	if len(stringo)>0:
	
		return stringo[0].upper() + stringo[1:]
	else:
		return stringo

for article in fileeopen:
	title, data = article
	dict = {}
	for it in data:
		#if it[0] in dict:
		#	pywikibot.output(article)
		if it[1]!='':#izmantoti tukši parametri: ['tēma2', '']
			dict.update({it[0]:it[1]})
		#pywikibot.output(dict)
	
	for itt in topiclist:
		if itt in dict:
			topics.append(first_upper(dict[itt]))
			
	for itt2 in countrylist:
		if itt2 in dict:
			countries.append(first_upper(dict[itt2]))

	if 'dalībnieks' in dict:
		users.append(first_upper(dict['dalībnieks']))

topict = make_table(topics,'topic')
countrtable = make_table(countries,'country')
usertable = make_table(users,'user')

#todo: Kopā konkursam iesniegti X raksti.

pagecont = """{{{{CEE Spring 2019 navigācija}}}}
== Konkursā iesniegtie raksti ==
{}

== Izveidotie raksti pēc autora ==
{}

== Izveidotie raksti pēc valsts/reģiona ==
{}

== Izveidotie raksti pēc tēmas ==
{}

[[Kategorija:CEE Spring 2019|Statistika]]
""".format(main_table(fileeopen),usertable,countrtable,topict)
#[[Attēls:CEES2018.svg|thumb|350px|Izveidotie raksti pēc dienas]]

site = pywikibot.Site("lv", "wikipedia")
articletitle = 'Vikipēdija:CEE Spring 2019/Statistika'
saglapa = pywikibot.Page(site,articletitle)

saglapa.text = pagecont

saglapa.save(summary='bots: atjaunināts (kopējais rakstu skaits: {})'.format(len(fileeopen)), botflag=False, minor=False)