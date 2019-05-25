#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pywikibot, re, mwparserfromhell
from pywikibot.exceptions import CoordinateGlobeUnknownException

import petsc

site = pywikibot.Site("lv", "wikipedia")
datasite = pywikibot.Site("wikidata", "wikidata")
repo = datasite.data_repository()


parselist = petsc.main('https://petscan.wmflabs.org/?language=lv&project=wikipedia&depth=0&categories=Latvijas%20ciemi&combination=subset&negcats=&ns%5B0%5D=1&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=no&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&templates_yes=&templates_any=&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&common_wiki=auto&source_combination=&wikidata_item=without&wikidata_label_language=&wikidata_prop_item_use=&wpiu=any&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&format=json&output_compatability=catscan&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=&al_commands=P31%3AQ532%0D%0AP17%3AQ211')

templateCheck = ['apdzīvotas vietas infokaste']

importedEnWikipedia = pywikibot.Claim(repo, u'P143')
enWikipedia = pywikibot.ItemPage(datasite, u'Q728945')
importedEnWikipedia.setTarget(enWikipedia)

def pagename(bg):
	bg = re.sub('\s*(\([^\(]+)$','',bg)
	
	return bg

def addPop(item,repo,iedzivotaji,y,m,d,iedzAts,lgia):
	#seriesprop = "P179"
	
	if y!='' and m!='' and d!='':
		pwbtime = pywikibot.WbTime(year=int(y), month=int(m), day=int(d))
	elif y!='' and (m=='' or d==''):
		pwbtime = pywikibot.WbTime(year=int(y))
	
	#iedz. skaits
	newClaim = pywikibot.Claim(repo, 'P1082')
	newClaim.setTarget(pywikibot.WbQuantity(amount=iedzivotaji, site=repo))
	item.addClaim(newClaim)
	
	#laika brīdis
	newClaim_date = pywikibot.Claim(repo, 'P585', isQualifier=True)
	newClaim_date.setTarget(pwbtime)
	newClaim.addQualifier(newClaim_date)
	
	if iedzAts =="yes" and lgia!='' and lgia.isnumeric:
		#apg. izteikts
		newClaim_ref = pywikibot.Claim(repo, 'P248', isReference=True)
		newClaim_ref.setTarget(pywikibot.ItemPage(repo, u'Q16362112'))
		
		#lgia id
		newClaim_ref2 = pywikibot.Claim(repo, 'P2496', isReference=True)
		newClaim_ref2.setTarget(lgia)
		
		#pārb datums @todo: izvilkt no atsauces
	#	newClaim_ref3 = pywikibot.Claim(repo, 'P813', isReference=True)
	#	newClaim_ref3.setTarget(pywikibot.WbTime(year=now.year, month=now.month, day=now.day))
		
	#	newClaim.addSources([newClaim_ref, newClaim_ref2, newClaim_ref3])
		newClaim.addSources([newClaim_ref, newClaim_ref2])

def addCoords(page,item):
	prop = 'P625'
	
	oldcoordinate = page.coordinates(primary_only=True)
	
	if oldcoordinate:
	
		claims = item.get().get('claims')
	
		coord_lat = float(oldcoordinate.lat)
		coord_long = float(oldcoordinate.lon)
		precision = 0.00027777777777778#1/100000
		target = pywikibot.Coordinate(coord_lat, coord_long, precision=precision, globe_item='http://www.wikidata.org/entity/Q2')
	
		newclaim = pywikibot.Claim(repo, prop)
		newclaim.setTarget(target)
		pywikibot.output(u'Adding %s, %s to %s' % (coord_lat,
							coord_long,
							item.title()))
						   
		try:
			item.addClaim(newclaim)

			newclaim.addSources([importedEnWikipedia])
		except CoordinateGlobeUnknownException as e:
			pywikibot.output(u'Skipping unsupported globe: %s' % e.args)
	
def simpleAdd(item,repo,prop,data):

	newClaim = pywikibot.Claim(repo,prop)
	newClaim.setTarget(data)
	item.addClaim(newClaim)
	newClaim.addSources([importedEnWikipedia])
	
def addname(item,repo,data):

	newClaim = pywikibot.Claim(repo,'P1705')#native label
	newClaim.setTarget(pywikibot.WbMonolingualText(text=data, language='lv'))
	item.addClaim(newClaim)
	#newClaim.addSources([importedEnWikipedia])
	
def datveidne(text):
	wikilink = re.compile('{{dat\|(\d+)\|(\d*)\|(\d*)\|\|bez}}')
	
	bearerM = wikilink.match(text)
	
	if bearerM:
		year = bearerM.group(1) or ''
		month = bearerM.group(2) or ''
		day = bearerM.group(3) or ''
				
		return year,month,day


def checkvalidlink(link):
	wikilink = re.compile('^\[\[([^\|\]]+)')
	
	bearerM = wikilink.match(link)
	
	if bearerM:
		linktowd = bearerM.group(1)
		#pywikibot.output(linktowd)
		brearTowd = pywikibot.Page(site,linktowd)
		
		if brearTowd.exists():
			if brearTowd.isRedirectPage():
				brearTowd = brearTowd.getRedirectTarget()
			if not brearTowd.isDisambig():
				valuereturn = brearTowd
			else:
				valuereturn = ''
	else:
		valuereturn = ''
				
	return valuereturn


def sanityvalue(value):
	value = re.sub('(\n|\r)', '',value)
	value = re.sub('\s\s+', ' ',value)
	value = re.sub('<!--.*?-->', '',value)#remove comments
	value = re.sub('<ref([^>]+)\/>', '',value)#remove self-closing reference tags
	value = re.sub('<ref((?!<\/ref>).)*<\/ref>', '',value)#remove references
	value = re.sub('<ref([^>]+)>', '',value)#remove reference tags
	
	return value

def createitem(ciems):
	nosaukums = pagename(ciems)
	data = {
		'labels': {
			'lv': { 'language': 'lv', 'value': nosaukums },
			'en': { 'language': 'en', 'value': nosaukums }
			},
		'sitelinks': {
			'lvwiki': {'site': 'lvwiki', 'title': ciems }
            }
		}
	item = pywikibot.ItemPage(datasite)
	summary = 'Bot: New item with sitelink from lvwiki'
	
	item.editEntity(data, summary=summary)
	
	return item
	

def main():
	for article in parselist:
		page = pywikibot.Page(site,article)
		
		#page = article
	
		if page.namespace() in [0,2]:
		
			articleTitle = page.title()
			pgnamebase = pagename(articleTitle)
			pywikibot.output("Working on %s" % articleTitle)
			item = createitem(articleTitle)
			item.get()
			
			ciems = pywikibot.ItemPage(datasite, u'Q532')
			latvija = pywikibot.ItemPage(datasite, u'Q211')
			
			simpleAdd(item,repo,'P31',ciems)
			
			simpleAdd(item,repo,'P17',latvija)
			
			text = page.get()
			wikicode = mwparserfromhell.parse(text)
			templates = wikicode.filter_templates()
		
			for tpl in templates:
				if tpl.name.lower().strip() in templateCheck:
					#Pagasts
					if tpl.has("subdivision_type2") and tpl.has("subdivision_name2"):
						pagaststips = tpl.get("subdivision_type2").value.strip()
						pagastsvert = tpl.get("subdivision_name2").value.strip()
					
						if pagaststips == 'Pagasts':
							print('ir pagasts')
							pagasts = checkvalidlink(pagastsvert)
							pywikibot.output(pagasts)
							
							simpleAdd(item,repo,'P131',pywikibot.ItemPage.fromPage(pagasts))
						
					#Attēls
					#Platība
					if tpl.has("var_id"):
						varid = tpl.get("var_id").value.strip()
						
						if varid!='' and varid.isnumeric:
							print('var is ok')
							
							simpleAdd(item,repo,'P2497',varid)
					
				
					if tpl.has("lgia_id"):
						lgiaid = tpl.get("lgia_id").value.strip()
						
						if lgiaid!='' and lgiaid.isnumeric:
							print('lgia is ok')
							
							simpleAdd(item,repo,'P2496',lgiaid)
						
					if tpl.has("postal_code_type") and tpl.has("postal_code"):
						paststips = tpl.get("postal_code_type").value.strip()
						pastsvert = tpl.get("postal_code").value.strip()
					
						if paststips == 'Pasta nodaļa':
							print('ir pasts')
							
							pastsvert = pastsvert.replace('LV-','')
							
							if pastsvert!='' and pastsvert.isnumeric:
								print('pasts is ok')
							
								simpleAdd(item,repo,'P281',pastsvert)
						
							
					if tpl.has("population_total"):
						iedzivotaji = tpl.get("population_total").value.strip()
						iedzivotaji = sanityvalue(iedzivotaji)
						
						if iedzivotaji!='':
							
							
							if tpl.has("population_as_of"):
								print('ir datums iedz.skaitam')
								iedzDat = tpl.get("population_as_of").value.strip()
								y,m,d = datveidne(iedzDat)
								print(y+''+m+''+d)
							
							else:
								iedzDat = ''
							
							if tpl.has("population_footnotes"):
								print('ir atsauce iedz.skaitam')
								iedzAts = tpl.get("population_footnotes").value.strip()
							else:
								iedzAts = ''
							
							if iedzAts.find('vietvardi.lgia.gov.lv/vv/to_www_ob') !=-1:
								print('lgia atsauce')
								iedzAts = 'yes'
							
							addPop(item,repo,iedzivotaji,y,m,d,iedzAts,lgiaid)
							
					break
			
			addname(item,repo,pgnamebase)
			addCoords(page,item)
	
'''redirects:
/w/api.php?action=query&format=json&prop=redirects&titles=Amilk%C4%81re+Ponkjelli&rdprop=pageid%7Ctitle

https://lv.wikipedia.org/wiki/Special:ApiSandbox#action=query&format=json&prop=redirects&titles=Amilk%C4%81re+Ponkjelli&rdprop=pageid%7Ctitle

nosaukums = "foo"

aliases = ['foobar']

list1 = ['foobar','foo (man)','foo','lorem']

def pagename(bg):
	bg = re.sub('\s*(\([^\(]+)$','',bg)
	
	return bg

#newlist = [re.sub('\s*(\([^\(]+)$','',f) for f in list1]
newlist = [pagename(f) for f in list1]
newlist = [f for f in newlist if f!=nosaukums and f not in aliases]
newlist = list(set(newlist))

print(newlist)
'''
						
if __name__ == "__main__":
	main()