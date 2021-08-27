import pywikibot, json

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

def do_all_labels(bigm,curr, filename):
	mymas1 = curr
	groupfd=0

	final = []
	for group in chunker(bigm,490):
		print(groupfd)
		groupfd += 1
		entis = one_query_labels(group)
		final.extend(entis)


	filedataREZ = open(filename, 'w', encoding='utf-8')
	#filedataREZ.write('\n'.join(['\t'.join(f) for f in final]))
	filedataREZ.write(json.dumps(final))
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

def get_labels_from_wikidata(items):
	#itemsforwork = [699590, 96621465, 20650885, 60693026, 23023435, 1708710, 56249797, 94534610, 20066885, 21225671, 10460434, 5173803, 10460450, 10459189, 40213701, 656616, 327681, 6221625, 59914562, 14831282, 368653, 95496234, 3547421, 1473264, 531302, 21513147, 35760470, 1420212, 11712125, 65853239, 56292964, 415178, 66827758, 16914548, 7896137, 27028154, 8834059, 32868159, 19794185, 20929885, 8557026, 30766538, 32380828, 8498453, 8417894, 13562384, 7854896, 9789405, 9298571, 7765651, 7496429, 7486711, 6902639, 7030091, 8800527, 8073857, 107312349, 18730703, 7583197, 8989807, 29245207, 7165202, 6408334, 7146093, 54271, 58213304, 251439, 3276983, 95502271, 573055, 16234878, 95503352, 103810656, 1085891, 10977348, 26195, 66606355, 23801389, 21223557, 388074, 21230400, 11832396, 3928977, 13557324, 245341, 105721755, 582280, 38053896, 1415446, 21220563, 3048989, 45123277, 107258209, 107368773, 76745, 1083159, 942931, 7893943, 12433018, 13606208, 7938121, 5658328, 4124229, 85813407, 29594225]
	itemsforwork = ["Q{}".format(f) for f in items if not str(f).startswith('Q')]

	#all_items_res = do_all_api(itemsforwork)
	#apires = open('personas-api-res.txt','w', encoding='utf-8')
	#apires.write(str(all_items_res))
	do_all_labels(itemsforwork,{}, 'no_lv_label.txt')

#
#main()
