import pywikibot, re, mwparserfromhell

import wdtools

site = pywikibot.Site("de", "wikipedia")

repo = site.data_repository()

importedEnWikipedia = pywikibot.Claim(repo,'P143')
enWikipedia = pywikibot.ItemPage(repo,'Q48183')
importedEnWikipedia.setTarget(enWikipedia)

templateCheck = ['transfermarkt','transfermarkt.de']

wdvalueConv = { 'spieler': 'P2446',
				'trainer': 'P2447'
				}

articles = wdtools.petscan('de','P2446,P2447',"Transfermarkt")

for article in articles:
	page = pywikibot.Page(site,article)
	#page = article
	
	if page.namespace() == 0:
		
		item = pywikibot.ItemPage.fromPage(page)
		
		articleTitle = page.title()
		pywikibot.output("Working on %s" % articleTitle)
		checkInst = wdtools.checkInstance('P31','Q5',item)
		
		if checkInst==True:
			text = page.get()
			wikicode = mwparserfromhell.parse(text)
			templates = wikicode.filter_templates()
		
			for tpl in templates:
				if tpl.name.lower().strip() in templateCheck:
					if tpl.has("TYP"):
						sector = tpl.get("TYP").value.lower().strip()
						if sector in wdvalueConv:
							prop = wdvalueConv[sector]
							if tpl.has("ID"):
								id = tpl.get('ID').value.strip()
								if len(id)>0:
									
									historycheck = wdtools.checkHist(item,id,prop)
									
									if historycheck==True:
										wdtools.addWD(prop,item,repo,id,importedEnWikipedia)
									
										break