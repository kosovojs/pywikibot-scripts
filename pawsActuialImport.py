import pywikibot, re, json, requests, os, sys, time
from datetime import datetime
#stActualImport.py

currenttime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
#print(currenttime)

filename = "IAAF-PAWS-fixed-"+str(currenttime)+".txt"
file = open(filename, "w", encoding='utf-8')

#prop = "P1146"

"""

    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+444)‎ . . Fukui Saki (Q50822706) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+346)‎ . . Fukui Saki (Q50822706) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+446)‎ . . (Q27862830) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+346)‎ . . (Q27862830) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+444)‎ . . (Q52160377) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+346)‎ . . (Q52160377) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+440)‎ . . Jayne Barnetson (Q50384715) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+346)‎ . . Jayne Barnetson (Q50384715) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+446)‎ . . (Q48761894) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+346)‎ . . (Q48761894) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+446)‎ . . Виктория Георгиевна Прокопенко (Q51668567) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.48 (izmaiņas | hronoloģija) . . (+346)‎ . . Виктория Георгиевна Прокопенко (Q51668567) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.47 (izmaiņas | hronoloģija) . . (+446)‎ . . Jonathan Varela Byrkjenes (Q16182863) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.47 (izmaiņas | hronoloģija) . . (+346)‎ . . Jonathan Varela Byrkjenes (Q16182863) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.47 (izmaiņas | hronoloģija) . . (+444)‎ . . (Q47667898) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.47 (izmaiņas | hronoloģija) . . (+346)‎ . . (Q47667898) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.47 (izmaiņas | hronoloģija) . . (+440)‎ . . Rio Maholtra (Q50363522) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.47 (izmaiņas | hronoloģija) . . (+346)‎ . . Rio Maholtra (Q50363522) ‎ (‎Created claim: IAAF identifikators (P1146): P1146)
    2018. gada 5. maijs, plkst. 10.47 (izmaiņas | hronoloģija) . . (+440)‎ . . Andreas Dimitrakis (Q22957468) ‎ (‎Added reference to claim: IAAF identifikators (P1146): P1146) (pēdējā izmaiņa)
    2018. gada 5. maijs, plkst. 10.47 (izmaiņas | hronoloģija) . . (+346)‎ . . Andreas Dimitrakis (Q22957468) ‎ (‎Created claim: IAAF identifikators (P1146): P1146) 
"""

def addWD(item,repo,prop,id,importedEnWikipedia):
	if item.claims:
		if 'P279' in item.claims: return 0
		
		if 'P31' in item.claims:
			instances = [wdClaimValue.getTarget().title() for wdClaimValue in item.claims['P31']]
			
			if (len(instances)>0 and 'Q5' not in instances):
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

#todo: validēt raksta nosaukumu ("x at olympics", 'list of')
#validēt id

def main():
	site = pywikibot.Site('wikidata', "wikidata")
	repo = site.data_repository()
	
	#['Q27051887', 'fl/else-flebbe-1', 'Q177837']
	
	
	begintime = time.time()
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	
	fileS = eval(open('Futbols-Python.txt', "r", encoding='utf-8').read())
	print('{} items left'.format(len(fileS)))
	
	
	counter = 0
	for parsingarticle in fileS:
		
		try:
			wditem,prop,value,wiki = parsingarticle
			
			regex = "[[Property:{}]]".format(prop)
			
			#print('--------------'+wditem+'--------------')
			
			#if wditem in ['Q52088043']: continue
			
			item = pywikibot.ItemPage(repo, wditem)#pywikibot.ItemPage.fromPage(page)
			####pywikibot.exceptions.IsRedirectPage
			
			try:
				item.get(get_redirect=True)
			except pywikibot.data.api.APIError:
				continue#fixme! - Q45367250
			except pywikibot.exceptions.OtherPageSaveError:
				continue#-Q52088043-
			#try:
			#	item.get()
			#except pywikibot.exceptions.IsRedirectPage:
			#	continue#fixme!
			
			#<class 'pywikibot.exceptions.IsRedirectPage'>
			
			#item = pywikibot.ItemPage(repo,pywikibot.Page(site,itemtitle))
			
			versions = item.getVersionHistory()
			Vcomments = [version.comment for version in versions]
			Vcomments2 = [version.comment for version in versions if regex in version.comment]
			file.write('{}\t{}\n'.format(wditem,'--frkmarker--'.join(Vcomments)))
			
			counter += 1
			
			if counter % 75 ==0:
				print(counter)
				sys.stdout.flush()
				time.sleep(35)
				
			
			if len(Vcomments2)==0:
				importedEnWikipedia = pywikibot.Claim(repo, 'P143')
				enWikipedia = pywikibot.ItemPage(repo, wiki)
				importedEnWikipedia.setTarget(enWikipedia)
		
				try:
					addWD(item,repo,prop,value,importedEnWikipedia)
				except pywikibot.data.api.APIError:
					continue#fixme! - Q45367250
				
			else:
				print('\t not ok')
		except:
			continue#-Q52088043-
			
				
main()