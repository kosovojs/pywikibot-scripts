import re, pywikibot, os
import toolforge
from customFuncs import get_quarry as quarry
from collections import Counter

site = pywikibot.Site("lv", "wikipedia")

conn = toolforge.connect('lvwiki_p','analytics')

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection = conn):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = connection.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows
#

SQLMAIN = """select page_title
from page
where page_is_redirect=0 and page_namespace=0"""

query_res = run_query(SQLMAIN,conn)

data = [encode_if_necessary(f[0]).replace('_',' ') for f in query_res]

lowercased_unique = Counter([f.lower() for f in data])

dublicates = sorted([f[0] for f in lowercased_unique.items() if f[1]>1])

#https://www.mediawiki.org/wiki/Manual:$wgLegalTitleChars
stringtocheck = "\"0-9A-Za-zĀČĒĢĪĶĻŅŠŪŽāčēģīķļņšūž\. ,!%\-\(\)—:'\/+&\?№ßö"

badthings = ['"',"'"]

regexr = "[^{}]".format(stringtocheck)

#titles = ['Ābece','Me*bele$s']

tosave = []

for title in data:
	if title[0] in badthings and title[-1] in badthings:
		#print('pēdiņas sākumā+beigās')
		tosave.append('pēdiņas sākumā+beigās')
	trt = re.findall(regexr,title)
	if trt:
		if '  ' in title:
			trt.append('divas atstarpes')
			#pywikibot.output(title)
		#tosave.append("* [[{}]]: {}".format(title,', '.join(trt)))#([title,trt])
	trt = re.findall('\d[-–]\d',title)
	if trt:
		tosave.append("* [[{}]]: {}".format(title,', '.join(trt)))#([title,trt])
#

for entry in dublicates:
	candidates = [f for f in data if f.lower() == entry]
	if len(candidates)>0:
		tosave.append("* {}: [[{}]]".format(entry,']], [['.join(candidates)))

page = pywikibot.Page(site,"Dalībnieks:Edgars2007/Nestandarta nosaukumi")
page.text = '\n'.join(tosave)
page.save(summary="upd", botflag=False)
