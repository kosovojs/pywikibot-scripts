import requests, json, pywikibot, re, os, datetime, mwparserfromhell
from bs4 import BeautifulSoup

templateCheck = "#invoke:sports table"
enwp = pywikibot.Site("en", "wikipedia")
lvwp = pywikibot.Site("lv", "wikipedia")

true = True
false = False
configuration = pywikibot.Page(lvwp,'Vikiprojekts:Futbols/Tabulas.json')
configuration = configuration.get()
configuration = eval(configuration)

mapper = configuration['articles']

botflag = configuration['botflag'] if 'botflag' in configuration else True

removeparams = configuration['remove']#note_res_KE varbūt arī nevajag ņemt ārā

site = pywikibot.Site('lv', 'wikipedia')

dict = {}

reslist = []

today = datetime.date.today()

def groupchange(enarticle):
	#enarticle = "Template:2016–17 Premier League table"
	enpage = pywikibot.Page(enwp,enarticle)
	entext = enpage.get()
	enwikicode = mwparserfromhell.parse(entext)
	templates = enwikicode.filter_templates()


	for tpl in templates:
		if tpl.name.lower().strip() in templateCheck:
			#pywikibot.output(tpl)

			for param in removeparams:
				if tpl.has(param):
					tpl.remove(param)

			newtext = str(tpl)

			for replace in configuration["repls"]:
				thisrepl = configuration["repls"][replace]
				newtext = newtext.replace(replace,thisrepl)

	return newtext

def dooutput(teams,res):
	teamLIST = teamlist2
	updatedate = today.strftime('{{dat|%Y|%m|%d||bez}}')
	wikitext = '''{{#invoke:Sporta tabula|main\n|source= \n\n|template_name=''' + tlname + '''\n''' + teams + '''\n''' + res + '''\n''' + teamLIST + '''\n}}<noinclude>\n[[Kategorija:Vikipēdijas veidnes]]\n</noinclude>'''

	return wikitext
#
def getCurrent(lvtext):
	currText = re.search('<!-- TABLE START -->\n(.*)\n<!-- TABLE END -->',lvtext, flags=re.DOTALL)

	if currText:
		return currText.group(1)

	return False


def doreplace(text,pretext,header,footer):
	newtext = re.sub(header + '.*' + footer, header + '\n' + pretext + '\n' + footer, text, flags=re.DOTALL)
	#pywikibot.output(newtext)

	return newtext
#
def main():

	for article in mapper:
		pywikibot.output("Working on %s" % article)
		lvtitle = mapper[article]
		page = pywikibot.Page(site,lvtitle)
		text = page.get()
		lvwikitable = getCurrent(text)
		enwikitable = article

		#if not lvwikitable: return 0#paziņot man

		returnedtext = groupchange(enwikitable)


		if returnedtext!=lvwikitable:
			tableInserted = doreplace(text,returnedtext,'<!-- TABLE START -->','<!-- TABLE END -->')

			page.text = tableInserted
			page.save(summary='Bots: atjaunināta tabula', botflag=True)
		else:
			print('no changes')

#
main()
