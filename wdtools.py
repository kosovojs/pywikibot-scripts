import requests
import json
import urllib.parse
import pywikibot

def quarry2(fileOpen):
	file2 = open(fileOpen, "r", encoding='utf-8')
	file2 = file2.read()

	json_data = json.loads(file2)
	#[f[0] for f in data["rows"]]
	
	return json_data["rows"]
	
def quarry(runid,counter='0'):
	url = "https://quarry.wmflabs.org/run/{}/output/{}/json".format(runid,counter)
	
	url2= requests.get(url)#.read()
	#pywikibot.output(url2.text)

	data = json.loads(url2.text)
	json_data = data
	return json_data["rows"]
	
def petscan(lang,prop,template):
	template = urllib.parse.quote(template)
	prop = urllib.parse.quote(prop)
	
	url = "https://petscan.wmflabs.org/?language={}&project=wikipedia&depth=0&categories=&combination=subset&negcats=&ns%5B0%5D=1&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=both&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&templates_yes={}&templates_any=&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&common_wiki=auto&source_combination=&wikidata_item=with&wikidata_label_language=&wikidata_prop_item_use={}&wpiu=none&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&format=json&output_compatability=catscan&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=tab_output".format(lang,template,prop)
	
	url2= requests.get(url)#.read()
	#pywikibot.output(url2.text)

	data = json.loads(url2.text)
	json_data = data

	#json_data = json.loads(file)

	#pywikibot.output(data)
	itemlist = json_data['*'][0]['a']['*']
	#pywikibot.output(itemlist)
	print('Found %s items on PetScan ' % len(itemlist))

	parselist = [item['title'] for item in itemlist]
	#for item in itemlist:
	#	enwikiarticle = item['title']
		#pywikibot.output(enwikiarticle)
	#	parselist.append(enwikiarticle)
		
	return parselist
	
def petscan2(cat,lang,prop,template):
	template = urllib.parse.quote(template)
	cat = urllib.parse.quote(cat)
	prop = urllib.parse.quote(prop)
	
	url = "https://petscan.wmflabs.org/?language={}&project=wikipedia&depth=0&categories={}&combination=subset&negcats=&ns%5B0%5D=1&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=both&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&templates_yes={}&templates_any=&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&common_wiki=auto&source_combination=&wikidata_item=with&wikidata_label_language=&wikidata_prop_item_use={}&wpiu=none&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&format=json&output_compatability=catscan&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=tab_output".format(lang,cat,template,prop)
	
	url2= requests.get(url)#.read()
	#pywikibot.output(url2.text)

	data = json.loads(url2.text)
	json_data = data

	#json_data = json.loads(file)

	#pywikibot.output(data)
	itemlist = json_data['*'][0]['a']['*']
	#pywikibot.output(itemlist)
	print('Found %s items on PetScan ' % len(itemlist))

	parselist = [item['title'] for item in itemlist]
	#for item in itemlist:
	#	enwikiarticle = item['title']
		#pywikibot.output(enwikiarticle)
	#	parselist.append(enwikiarticle)
		
	return parselist
	
	
def petscan3(lang,cat,template):
	template = urllib.parse.quote(template)
	cat = urllib.parse.quote(cat)
	
	url = "https://petscan.wmflabs.org/?language={}&project=wikipedia&depth=0&categories={}&combination=subset&negcats=&ns%5B0%5D=1&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=both&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&templates_yes=&templates_any={}&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&common_wiki=auto&source_combination=&wikidata_item=with&wikidata_label_language=&wikidata_prop_item_use=&wpiu=none&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&format=json&output_compatability=catscan&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=tab_output".format(lang,cat,template)
	
	url2= requests.get(url)#.read()
	#pywikibot.output(url2.text)

	data = json.loads(url2.text)
	json_data = data

	#json_data = json.loads(file)

	#pywikibot.output(data)
	itemlist = json_data['*'][0]['a']['*']
	#pywikibot.output(itemlist)
	print('Found %s items on PetScan ' % len(itemlist))

	parselist = [item['title'] for item in itemlist]
	#for item in itemlist:
	#	enwikiarticle = item['title']
		#pywikibot.output(enwikiarticle)
	#	parselist.append(enwikiarticle)
		
	return parselist
	
def petscanOR(url):
	#template = urllib.parse.quote(template)
	#cat = urllib.parse.quote(cat)
	
	#url = "https://petscan.wmflabs.org/?language={}&project=wikipedia&depth=0&categories={}&combination=subset&negcats=&ns%5B0%5D=1&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=both&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&templates_yes=&templates_any={}&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&common_wiki=auto&source_combination=&wikidata_item=with&wikidata_label_language=&wikidata_prop_item_use=&wpiu=none&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&format=json&output_compatability=catscan&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=tab_output".format(lang,cat,template)
	
	url2= requests.get(url)#.read()
	#pywikibot.output(url2.text)

	data = json.loads(url2.text)
	json_data = data

	#json_data = json.loads(file)

	#pywikibot.output(data)
	itemlist = json_data['*'][0]['a']['*']
	#pywikibot.output(itemlist)
	print('Found %s items on PetScan ' % len(itemlist))

	parselist = [item['title'] for item in itemlist]
	#for item in itemlist:
	#	enwikiarticle = item['title']
		#pywikibot.output(enwikiarticle)
	#	parselist.append(enwikiarticle)
		
	return parselist
	
#def importFromEnwiki():
	

def checkInstance(propC,itemC,item):
	#checkInstance('P31','Q5',item)
	
	if item.claims and propC in item.claims:
		instances = [wdClaimValue.getTarget().title() for wdClaimValue in item.claims[propC]]
		
		if itemC in instances:
			return True
		else:
			####################logme(itemtitle,id,'No Q5 in P31')
			return False
			
	else:
		#logme
		print('no P31, logging')
		################################logme(itemtitle,id,'No P31')
		return False
		#return True
		
def addWD(prop,item,repo,id,importedEnWikipedia):
	if item.claims:
	
		if prop not in item.claims:
		
			claim = pywikibot.Claim(repo,prop)
			claim.setTarget(id)
			print('Adding claim')
			item.addClaim(claim)
			claim.addSources([importedEnWikipedia])
	else:
		claim = pywikibot.Claim(repo,prop)
		claim.setTarget(id)
		print('Adding claim')
		item.addClaim(claim)
		claim.addSources([importedEnWikipedia])

def checkHist(item,id,prop):
	revisions = item.getVersionHistory()
	
	regex = "[[Property:%s]]: %s" % (prop,id)
	
	comments = [version.comment for version in revisions if regex in version.comment]
	if len(comments)==0:
		return True
	else:
		#####################logme(itemtitle,id,'Already was in item')
		return False
	