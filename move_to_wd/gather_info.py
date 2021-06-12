import pywikibot

import re, pywikibot, urllib.parse, requests, os
from datetime import date

petsc = False

all_items_to_labels = []

def clean_api(thisitemdata):
	toret = {}

	theseclaims1 = thisitemdata['claims']
	for prop in theseclaims1:
		thisprop = theseclaims1[prop]
		if prop=='P1087': continue#elo rangs

		theseclaims = []

		for claim in thisprop:
			claimtosave = None
			datatype = claim['mainsnak']['datatype']
			if 'datavalue' in claim['mainsnak']:
				if datatype in ('external-id','string','commonsMedia','url'):
					claimtosave = claim['mainsnak']['datavalue']['value']
				elif datatype=='wikibase-item':
					claimtosave = claim['mainsnak']['datavalue']['value']['id']
					all_items_to_labels.append(claimtosave)
				elif datatype=='time':
					claimtosave = claim['mainsnak']['datavalue']['value']['time']+'/'+str(claim['mainsnak']['datavalue']['value']['precision'])
				elif datatype=='quantity':
					claimtosave = claim['mainsnak']['datavalue']['value']['amount']+'U'+str(claim['mainsnak']['datavalue']['value']['unit'].replace('http://www.wikidata.org/entity/Q',''))
					all_items_to_labels.append(claim['mainsnak']['datavalue']['value']['unit'].replace('http://www.wikidata.org/entity/',''))
				elif datatype=='monolingualtext':
					claimtosave = claim['mainsnak']['datavalue']['value']['language']+': '+claim['mainsnak']['datavalue']['value']['text']
				else:
					print(datatype)

				theseclaims.append(claimtosave)
		toret[prop] = theseclaims

	return toret
#

def petscan(tpl,language):
	if petsc:
		r = requests.get('https://petscan.wmflabs.org/?language='+language+'&project=wikipedia&depth=0&categories=&combination=subset&negcats=&ns%5B0%5D=1&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=both&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&templates_yes='+urllib.parse.quote(tpl)+'&templates_any=&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&subpage_filter=either&common_wiki=auto&source_combination=&wikidata_item=any&wikidata_label_language=&wikidata_prop_item_use=&wpiu=any&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&labels_yes=&cb_labels_yes_l=1&langs_labels_yes=&labels_any=&cb_labels_any_l=1&langs_labels_any=&labels_no=&cb_labels_no_l=1&langs_labels_no=&format=json&output_compatability=catscan&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=tab_output')
		r.encoding = 'utf-8'
		json_data = eval(r.text)['*'][0]['a']['*']

	else:
		json_data = eval(open('personas-petscan-input.txt','r', encoding='utf-8').read())['*'][0]['a']['*']

	toret = [d['q'] for d in json_data if 'q' in d]

	return toret
#
site = pywikibot.Site("wikidata", "wikidata")
site.login()

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#

def doAPI(wditems):
	r = ''
	idlist = '|'.join(wditems)
	r = pywikibot.data.api.Request(site=site, action="wbgetentities",
									props="claims", ids=idlist,redirects='yes').submit()

	#pywikibot.output(r)
	return r
#

def do_all_api(bigm):
	object = {}
	groupfd=0

	for group in chunker(bigm,490):
		print(groupfd)
		groupfd += 1
		entis = doAPI(group)['entities']
		entitylist = entis.keys()

		for entdata in entitylist:
			object.update({entdata:clean_api(entis[entdata])})

	return object
#

def do_all_labels(bigm,curr):
	mymas1 = curr
	groupfd=0

	final = []
	for group in chunker(bigm,490):
		print(groupfd)
		groupfd += 1
		entis = one_query_labels(group)
		final.extend(entis)


	filedataREZ = open('lvinfoboxes-labels.txt', 'w', encoding='utf-8')
	filedataREZ.write('\n'.join(['\t'.join(f) for f in final]))
#

def one_query_labels(items):
	items = [f for f in items if f.startswith('Q')]
	r = pywikibot.data.api.Request(site=site, action="wbgetentities", format='json', ids='|'.join(items), redirects='yes', props="labels|sitelinks").submit()
	#
	masiv = processres_labels(r)

	return masiv
#
def processres_labels(realdata):
	masivcs = {}
	lv_nos = {}

	for entry in realdata["entities"]:
		#if entry
		try:
			dat = realdata["entities"][entry]["labels"]
		except KeyError:
			#print(entry)
			continue
			#dat = {}

			#{'nl': {'value': 'János Bagócs', 'language': 'nl'}, 'en': {'value': 'János Bagócs', 'language': 'en'}}
		masivcs.update({entry:{f:dat[f]['value'] for f in dat if f == 'en'}})
		lv_nos.update({entry:realdata["entities"][entry]["sitelinks"]["lvwiki"]['title']})

	res = []

	for entry in lv_nos:
		entitle = masivcs.get(entry).get('value') or ''
		res.append([entry, entitle, lv_nos[entry]])
	return res
#

def main():
	itemsforwork = [12804359, 309316, 497028, 309318, 573225, 500074, 245202, 500084, 392535, 219384, 497052, 330686, 16070003, 407448, 60693026, 516824, 85859539, 23023435, 20028411, 4149782, 59282938, 85971923, 12784635, 544464, 24010829, 16483470, 24035750, 1359850, 1048589, 12273992, 20432493, 65262842, 11774288, 474886, 51583, 461031, 260463, 13416787, 181936, 3380035, 12870016, 20570861, 29564928, 9284826, 4501731, 11712125, 27588583, 1536377, 8253, 2073192, 8148194, 8148707, 8151524, 8153768, 6580205, 8147663, 9774002, 96195486, 6562475, 6669087, 10226981, 32868159, 19794185, 27028154, 32420975, 20929885, 9718435, 7484012, 7583006, 8765052, 8825661, 8825662, 8529285, 7372335, 6563815, 32380828, 30766538, 8588316, 13562384, 7854896, 7282461, 6211172, 8748214, 8800527, 7145336, 8895505, 29245207, 7583197, 8989807, 7646649, 8197037, 8967533, 14396115, 97595981, 1431487, 58213304, 1139983, 830521, 623699, 729788, 22360, 2426861, 935886, 660082, 158816, 12221772, 15935085, 15625039, 343130, 4146872, 16408504, 17637064, 10977348, 1431486, 7116609, 12501562, 43384100, 842755, 1351303, 1156601, 54507123, 927731, 28106966, 1206521, 1207258, 22110899, 10646849, 18738700, 13557324, 1166159, 1886126, 678565, 2480013, 105435536, 2604517, 321458, 158205, 4417772, 65772506, 97769209, 21111316, 1635369, 45123277, 22279, 645234, 1161666, 561315, 694050, 154037, 12297030, 16710407, 16355264, 2668009, 1126240, 12981661, 12433018, 6312450, 6593852, 13606208, 8128019, 13361503, 360417, 259313, 201805, 1550905, 21346306, 143330, 178213]
	itemsforwork = ["Q{}".format(f) for f in itemsforwork]

	#all_items_res = do_all_api(itemsforwork)
	#apires = open('personas-api-res.txt','w', encoding='utf-8')
	#apires.write(str(all_items_res))

	get_labels = do_all_labels(itemsforwork,{})

#
main()
