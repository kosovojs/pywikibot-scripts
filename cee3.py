import pywikibot, re, mwparserfromhell, customFuncs, os
from pywikibot import textlib
from wdtools import petscanOR as petsc

#os.chdir(r'projects/cee')


filetowrite1 = open('cee2dfgfdfgdfgdfgdgdfgd-2-final.txt','r', encoding='utf-8')
fileconts = eval(filetowrite1.read())
#fileconts = []
filetowrite1.close()
articles_alreadsy = [f[0] for f in fileconts]
#kategorijas - skatīt pāradresācijas -> dictionary @ python


site = pywikibot.Site("lv", "wikipedia")
def getparam(tlobject,params):
	for param in params:
	
		if tlobject.has(param):
			opficmlapa = tlobject.get(param).value.strip()
					
			if opficmlapa!='':
			
				return opficmlapa
				break
		
		#else:
	return False
#
articles = petsc('https://petscan.wmflabs.org/?language=lv&project=wikipedia&depth=0&categories=&combination=subset&negcats=&ns%5B1%5D=1&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=both&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&templates_yes=CEE%20Spring%202019&templates_any=&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&subpage_filter=either&common_wiki=cats&source_combination=&wikidata_item=no&wikidata_label_language=&wikidata_prop_item_use=&wpiu=any&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&labels_yes=&cb_labels_yes_l=1&langs_labels_yes=&labels_any=&cb_labels_any_l=1&langs_labels_any=&labels_no=&cb_labels_no_l=1&langs_labels_no=&format=json&output_compatability=catscan&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=tab_output')#['Diskusija:Zengē']






print(len(articles))

diff = list(set(articles)-set(articles_alreadsy))
print(len(diff))

tplnames_en = ['cee spring 2019']

fsdf = []

for article in diff:
	
	page = pywikibot.Page(site,"Diskusija:{}".format(article))
	pagetext = page.get()
	#wikicode = mwparserfromhell.parse(pagetext)
	#templates = wikicode.filter_templates()
	
	for template, fielddict in textlib.extract_templates_and_params(pagetext, remove_disabled_parts=False, strip=True):
		tplname = template.lower().strip().replace('_',' ')
			
		if tplname not in tplnames_en:
			continue
			
		fielditems = [[k[0],k[1]] for k in fielddict.items()]
		
		fsdf.append([article,fielditems])
		break
#
#pywikibot.output(fsdf)
fileconts.extend(fsdf)

with open('cee2dfgfdfgdfgdfgdgdfgd-2-final.txt','w', encoding='utf-8') as filetowrite1:
	filetowrite1.write(str(fileconts))