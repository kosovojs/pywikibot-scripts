#!/usr/bin/python
# coding=utf8
'''
Author: Edgars Košovojs

'''
import pywikibot, re
from datetime import date, datetime, timedelta

botflag = False

daycounttoinclude = 8#cik dienām ģenerēt aprakstu

lvsite = pywikibot.Site("lv", "wikipedia")#, user='Edgars2007'
commons = pywikibot.Site("commons", "commons")

def getdata():
	files = []
	firstday = datetime.now()# + timedelta(days=1)
	#print(firstday)

	for dayADD in range(daycounttoinclude):
		daytoprint = (firstday + timedelta(days=dayADD)).date()
		day = daytoprint.strftime("%Y-%m-%d")
		#day = '{d.year}-{d.month}-{d.day}'.format(d=daytoprint)
		#'{d.month}/{d.day}/{d.year}'.format(d=datetime.datetime.now())

		dayP = '|%s=-switchstart-<!--\n          -->|file=[[Attēls:{{Potd/%s}}|320x320px]]<!--\n          -->|endesc={{Potd/%s (en)}}<!--\n          -->|lvdesc=--switchend-' % (day,day,day)

		files.append(dayP)

	return files

def main():
	wikitext = getdata()

	text = '\n'.join(wikitext)

	r = pywikibot.data.api.Request(site=commons, action='expandtemplates', format='json', text=text,
									prop='wikitext', includecomments=1).submit()

	output = r['expandtemplates']['wikitext']

	output = output.replace('-switchstart-','{{#switch:{{{2|}}}').replace('--switchend-','}}').replace('&nbsp;',' ')
	output = re.sub('\[\[:(en|w(:en)?|Category):([^\|]+\|)?([^\]]+)\]\]',r'\4',output)#uzlabot?
	#output = re.sub('\[\[:en:([^\|]+\|)?([^\]]+)\]\]',r'\2',output)

	output = '{{#switch:{{{1|}}}\n'+output+'\n}}'

	pagetosave = pywikibot.Page(lvsite,'Veidne:Commons dienas bilde/Dati/Smilšu kaste')
	pagetosave.text = output
	pagetosave.save(summary='bots: atjaunināts', botflag=botflag, minor=False)#, as_group='sysop'


if __name__ == "__main__":
	main()
