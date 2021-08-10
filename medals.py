import requests, json, pywikibot, re, os, datetime, mwparserfromhell
from bs4 import BeautifulSoup

#os.chdir(r'projects/sportsTables')

templateCheck = "medals table"
enwp = pywikibot.Site("en", "wikipedia")
lvwp = pywikibot.Site("lv", "wikipedia")

configuration = {
	"Fake komentārs": "STOP un botflag der 'true' vai 'false' (bez pēdiņām)",
	"STOP": False,
	"botflag": True,
	"remove": [
		"event",
		"team",
		"show_limit"
	],
	"articles": {
		"2020 Summer Olympics medal table": "2020. gada vasaras olimpisko spēļu medaļu tabula"
	},
	"prop_values": {
		"remaining_link": "Pārējās valstis"
	},
	"repls": {
		"2020 Summer Olympics medal table": "2020. gada olimpisko spēļu medaļu kopvērtējums",
		"Host nation (Japan)": "Mājinieki (Japāna)",
		"[[2020 Summer Olympics medal table#Medal table|Remaining NOCs]]": "Pārējās valstis",
		"[[2020. gada olimpisko spēļu medaļu kopvērtējums#Medal table|Remaining NOCs]]": "Pārējās valstis",
		"[[2020. gada olimpisko spēļu medaļu kopvērtējums#Medal table|Remaining NOCs]]": "Pārējās valstis",
		"[[2020. gada olimpisko spēļu medaļu kopvērtējums#Medal table|Remaining Teams]]": "Pārējās valstis",
		"[[2020 Summer Olympics medal table#Medal table|Remaining Teams]]": "Pārējās valstis",
		"flagIOCteam": ""
	}
}


mapper = configuration['articles']

botflag = configuration['botflag'] if 'botflag' in configuration else True

removeparams = configuration['remove']#note_res_KE varbūt arī nevajag ņemt ārā
paramsToReplace = configuration['prop_values']#note_res_KE varbūt arī nevajag ņemt ārā

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

			for param in paramsToReplace:
				if tpl.has(param):
					val = paramsToReplace.get(param)
					tpl.remove(param)
					tpl.add(param, val)

			newtext = str(tpl)

			for replace in configuration["repls"]:
				thisrepl = configuration["repls"][replace]
				newtext = newtext.replace(replace,thisrepl)

	return newtext

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
		if 'nobots' in text: return

		lvwikitable = getCurrent(text)
		enwikitable = article

		#if not lvwikitable: return 0#paziņot man

		returnedtext = groupchange(enwikitable)

		change = len(returnedtext) - len(lvwikitable)
		print(change)

		useBotFlag = False if change > 500 else True


		if returnedtext!=lvwikitable:
			tableInserted = doreplace(text,returnedtext,'<!-- TABLE START -->','<!-- TABLE END -->')

			page.text = tableInserted
			page.save(summary='Bots: atjaunināta tabula', botflag=useBotFlag)
		else:
			print('no changes')

#
main()
