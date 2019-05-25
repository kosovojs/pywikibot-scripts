import pywikibot, re, toolforge, sys, os, customFuncs

#os.chdir(r'projects/comcat')
sources = eval(open(r'wikieditions.json', 'r', encoding='utf-8').read())

WIKI = 'ruwiki'

site = pywikibot.Site('wikidata', "wikidata")
commons = pywikibot.Site('commons', "commons")
repo = site.data_repository()

prop = 'P373'

wiki_site_object = None#pywikibot.Site()


#page_id	page_namespace	page_title	page_restrictions	page_is_redirect	page_is_new	page_random	page_touched	page_links_updated	page_latest	page_len	page_content_model	page_lang	iwl_from	iwl_prefix	iwl_title	pp_page	pp_propname	pp_value	pp_sortkey	page_id	page_namespace	page_title	page_restrictions	page_is_redirect	page_is_new	page_random	page_touched	page_links_updated	page_latest	page_len	page_content_model	page_lang	pl_from	pl_namespace	pl_title	pl_from_namespace

#pp.pp_value as WDitem, iwl_title as category,
sqlQuery = """SELECT wp.page_id as pageID, wp.page_title as pageTitle, iwl_title as category, pp.pp_value as WDitem, 
    (select ips_site_page from wikidatawiki_p.wb_items_per_site where ips_site_id="commonswiki" and ips_item_id=SUBSTR(pp.pp_value,2)) as categ
FROM page AS wp
JOIN iwlinks ON iwl_from = wp.page_id
LEFT JOIN page_props AS pp
  ON pp.pp_page = wp.page_id AND pp.pp_propname = 'wikibase_item'
LEFT JOIN wikidatawiki_p.page AS wdp
  ON wdp.page_title = pp.pp_value AND wdp.page_namespace = 0
LEFT JOIN wikidatawiki_p.pagelinks AS wdpl
  ON wdpl.pl_from = wdp.page_id AND wdpl.pl_namespace = 120 AND wdpl.pl_title = 'P373'
WHERE wp.page_namespace = 0
AND iwl_prefix='commons' and iwl_title like "Category:%"
AND wdpl.pl_from IS NULL"""
#
cursorCache = {}
#
def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#
def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(sql_query,connectionObj):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = connectionObj.cursor()
		cursor.execute(sql_query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#
#todo: jāpabeidz
def getConnectionObj(objectToCheck):
	if objectToCheck:
		return objectToCheck
	
	#return 
#
def checkCommonscatLink(name=''):
	"""Return the name of a valid commons category.
	If the page is a redirect this function tries to follow it.
	If the page doesn't exists the function will return an empty string
	"""
	name = name.replace('Category:','')
	pywikibot.log('getCommonscat: ' + name)
	try:
		#commonsSite = site.image_repository()
		# This can throw a pywikibot.BadTitle
		#print(name)
		commonsPage = pywikibot.Page(commons, 'Category:' + name)

		if not commonsPage.exists():
			pywikibot.output('Commons category does not exist. '
								'Examining deletion log...')
			logpages = commons.logevents(logtype='delete',
												page=commonsPage)
			for logitem in logpages:
				loguser = logitem.user()
				logcomment = logitem.comment()
				# Some logic to extract the target page.
				regex = (
					r'moved to \[\[\:?Category:'
					r'(?P<newcat1>[^\|\}]+)(\|[^\}]+)?\]\]|'
					r'Robot: Changing Category:(.+) '
					r'to Category:(?P<newcat2>.+)')
				m = re.search(regex, logcomment, flags=re.I)
				if m:
					if m.group('newcat1'):
						return checkCommonscatLink(m.group('newcat1'))
					elif m.group('newcat2'):
						return checkCommonscatLink(m.group('newcat2'))
				else:
					pywikibot.output(
						"getCommonscat: {} deleted by {}. Couldn't find "
						'move target in "{}"'
						.format(commonsPage, loguser, logcomment))
					return ''
			return ''
		elif commonsPage.isRedirectPage():
			pywikibot.log('getCommonscat: The category is a redirect')
			return checkCommonscatLink(
				commonsPage.getRedirectTarget().title(with_ns=False))
		elif (pywikibot.Page(commons,
				'Template:Category redirect') in commonsPage.templates()):
			pywikibot.log(
				'getCommonscat: The category is a category redirect')
			for template in commonsPage.templatesWithParams():
				if (
					template[0].title(with_ns=False) == 'Category redirect'
					and len(template[1]) > 0
				):
					return checkCommonscatLink(template[1][0])
		elif commonsPage.isDisambig():
			pywikibot.log('getCommonscat: The category is disambiguation')
			return ''
		else:
			return commonsPage.title(with_ns=False)
	except pywikibot.BadTitle:
		# Funky title so not correct
		return ''
#
def getDataFromDB(wikiLang):
	conn = toolforge.connect(wikiLang+'wiki_p','analytics')

	queryRES = run_query(sqlQuery, conn)
	queryRES = [[encode_if_necessary(f) for f in fileSaver] for fileSaver in queryRES]

	with open('comcat_ex_'+wikiLang+'.txt','w',encoding='utf-8') as fileS:
		fileS.write(str(queryRES))
	
	return queryRES
#
def checkIfCommonsCategoryHasBeenUsedQuery(commCats):
	itemTpl = '"' + '" "'.join([f for f in commCats if '"' not in f]) + '"'
	sparQueryText = 'select ?val { values ?val {     '+itemTpl+'     } ?item wdt:P373 ?val . }'
	sparqlRes = customFuncs.basic_sparql(sparQueryText)

	items = set([f["val"]["value"] for f in sparqlRes])
	
	return set(commCats) - items

def checkIfCommonsCategoriesHasNotBeenUsedInBatches(commonsCategoryList):
	allCommonsCategoriesThatHasNOTBeenUsed = []
	for chunk in chunker(commonsCategoryList, 50):
		thispart = checkIfCommonsCategoryHasBeenUsedQuery(chunk)
		allCommonsCategoriesThatHasNOTBeenUsed.extend(thispart)
	
	return allCommonsCategoriesThatHasNOTBeenUsed
#
def parseDBResults(inputData):
	allData = {}
	categoriesToImport = []
	for one in inputData:
		# wp.page_id as pageID, wp.page_title as pageTitle, iwl_title as category, pp.pp_value as WDitem,  categ
		pageId, pageTitle, categoryToImport, wditem, categoryToCheck = one
		
		categoryToImport = categoryToImport.replace('Category:','').replace('_',' ')
		if categoryToImport=='': continue
		if categoryToCheck: continue
		if not wditem: continue
		
		categoriesToImport.append(categoryToImport)

		if wditem in allData:
			allData[wditem].append([categoryToImport, pageId, pageTitle, wditem])
		else:
			allData[wditem] = [[categoryToImport, pageId, pageTitle, wditem]]
	#
	allData = [allData[f][0] for f in allData if len(allData[f])==1]#+jānočeko, vai attiecīgā commons kategorija ir piedāvāta tikai vienu reizi
	return allData

def addWD(item,repo,id,importedEnWikipedia):
	if prop in item.claims: return 0
	if item.claims:
		if 'P279' in item.claims: return 0
		
		if 'P31' in item.claims:
			instances = [wdClaimValue.getTarget().title() for wdClaimValue in item.claims['P31']]
			
			if (len(instances)>0 and 'Q13406463' in instances):#Q13406463) - wikimedia saraksts
				return

		if prop not in item.claims:
		
			claim = pywikibot.Claim(repo,prop)
			claim.setTarget(id)
			item.addClaim(claim)
			claim.addSources([importedEnWikipedia])
	else:
		claim = pywikibot.Claim(repo,prop)
		claim.setTarget(id)
		item.addClaim(claim)
		claim.addSources([importedEnWikipedia])

def parseOneArticle(commonsTitle, wdItem):
	finalTitle = checkCommonscatLink(commonsTitle)

	if finalTitle=='': return

	item = pywikibot.ItemPage(repo, wdItem)
	item.get(get_redirect=True)
	importedEnWikipedia = pywikibot.Claim(repo, 'P143')
	enWikipedia = pywikibot.ItemPage(repo, 'Q'+str(sources[WIKI]))
	importedEnWikipedia.setTarget(enWikipedia)

	addWD(item,repo,finalTitle,importedEnWikipedia)

def main():
	dataFromDB = eval(open('comcat_ex_ru.txt','r',encoding='utf-8').read())#getDataFromDB('ru')
	parsedResults = parseDBResults(dataFromDB)

	getAllCommonsCategories = [f[0] for f in parsedResults][:50]
	goodCommonsCategories = checkIfCommonsCategoriesHasNotBeenUsedInBatches(getAllCommonsCategories)
	with open('comcat_ex_good_cats.txt','w',encoding='utf-8') as fileS:
		fileS.write(str(goodCommonsCategories))

	for one_entry in parsedResults[:50]:
		categoryToImport, pageId, pageTitle, wditem = one_entry
		if categoryToImport not in goodCommonsCategories: continue
		parseOneArticle(categoryToImport, wditem)

	#with open('comcat_ex_2.txt','w',encoding='utf-8') as fileS:
	#	fileS.write(str(parsedResults))
#
main()