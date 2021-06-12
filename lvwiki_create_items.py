import pywikibot, os, re, requests, time

#file2 = eval(open("ltuciemi.txt", "r", encoding='utf-8').read())


def pagename(bg):
	bg = re.sub(r'\s*(\([^\(]+)$', '', bg)

	return bg


def ref(prop, val):
	refer = [{
		"snaks": {
			"P" + prop: [{
				"snaktype": "value",
				"property": "P" + prop,
				"datavalue": {
					"value": {
						"id": val,
						"entity-type": 'item'
					},
					"type": "wikibase-entityid"
				}
			}]
		}
	}]

	return refer


#


def basic_petscan_obj(data):
	#http://petscan.wmflabs.org/?psid=157563&format=json
	#payload = {
	#	'psid': id,
	#	'format': 'json'
	#}
	data.update({'format': 'json'})

	r = requests.get('http://petscan.wmflabs.org/?', params=data)
	r.encoding = 'utf-8'
	json_data = eval(r.text)

	#items = [f["item"]["value"].replace('http://www.wikidata.org/entity/','') for f in json_data['results']['bindings']]

	return json_data['*'][0]['a']['*']

def createitem(ciems):
	nosaukums = pagename(ciems.replace('_', ' '))
	data = {
		'labels': {
			'lv': {
				'language': 'lv',
				'value': nosaukums
			}
		},
		'sitelinks': {
			'lvwiki': {
				'site': 'lvwiki',
				'title': ciems
			}
		}
	}
	return data


#
def get_from_petscan(cats, dept):
	payl = {
		'categories': cats,
		'language': 'lv',
		'project': 'wikipedia',
		'doit': 'Do it!',
		'common_wiki': 'auto',
		'depth': dept,
		'output_compatability': 'catscan',
		'ns[0]': '1',
		'combination': 'subset',
		'wikidata_item': 'without'
	}

	articlelist = basic_petscan_obj(payl)
	articles = [f['title'] for f in articlelist]
	#https://petscan.wmflabs.org/?language=lv&project=wikipedia&depth=0&categories=Ielas%20R%C4%ABg%C4%81%20p%C4%93c%20alfab%C4%93ta&combination=subset&negcats=&ns%5B0%5D=1&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=no&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&page_image=any&ores_type=any&ores_prob_from=&ores_prob_to=&ores_prediction=any&templates_yes=&templates_any=&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&subpage_filter=either&common_wiki=auto&source_combination=&wikidata_item=without&wikidata_label_language=&wikidata_prop_item_use=&wpiu=any&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&labels_yes=&cb_labels_yes_l=1&langs_labels_yes=&labels_any=&cb_labels_any_l=1&langs_labels_any=&labels_no=&cb_labels_no_l=1&langs_labels_no=&format=json&output_compatability=catscan&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=tab_output
	return articles


def one_claim(prop, value):
	#if prop=='P131':
	datavalue = {
		"type": "wikibase-entityid",
		"value": {
			"entity-type": 'item',
			"id": value
		}
	}
	#else:
	#	datavalue = {"type":"quantity" , "value":{"amount":value,"unit":"1"}}

	thisclaim = {
		'mainsnak': {
			"snaktype": "value",
			"property": prop,
			"datavalue": datavalue,
			"datatype": "wikibase-item"
		},
		"type": "statement",
		"rank": "normal",
		"references": ref('143', 'Q728945')  #https://www.wikidata.org/wiki/
	}

	return thisclaim


#
claimvals = [{
	'prop': 'P131',
	'val': 'Q123'
}, {
	'prop': 'P1082',
	'val': 8,
	'year': '2011'
}]

site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()


def one_item(ciems, claims, descrips):
	nosaukums = pagename(ciems.replace('_', ' '))
	item = pywikibot.ItemPage(site)
	summary = 'Bot: New item with sitelink from [[Q728945]] + adding data ({})'

	data = claims

	data2 = {
		'labels': {
			'lv': {
				'language': 'lv',
				'value': nosaukums
			}
		},
		'descriptions': descrips,
		'sitelinks': {
			'lvwiki': {
				'site': 'lvwiki',
				'title': ciems
			}
		}
	}

	finalclaims = {}
	allprops = []
	for entry in data:
		prop = entry['prop']
		value = entry['val']
		allprops.append(prop)
		finalclaims.update({prop: [one_claim(prop, value)]})
	#
	allprops = list(set(allprops))
	allprops = sorted(allprops, key=lambda x: int(x[1:]))  #natsorted(allprops)
	allprops = ['[[Property:{}]]'.format(f) for f in allprops]

	data2.update({'claims': finalclaims})

	try:
		item.editEntity(data2, summary=summary.format(', '.join(allprops)))
		time.sleep(1)
		#pywikibot.output(values)
	except:
		pywikibot.output(ciems)
		return 0
	#item.editEntity({'claims':finalclaims}, summary='adding data ({}) from [[Q202472]]'.format(', '.join(allprops)))


#
jsonobj = [{
	'cat':
	'Ielas Rīgā pēc alfabēta',
	'dep':
	'0',
	'name':
	'Rīgas ielas',
	'claims': [{
		'prop': 'P31',
		'val': 'Q79007'
	}, {
		'prop': 'P17',
		'val': 'Q211'
	}, {
		'prop': 'P131',
		'val': 'Q1773'
	}],
	'descs': {
		'lv': {
			'language': 'lv',
			'value': 'iela Rīgā'
		},
		'en': {
			'language': 'en',
			'value': 'street in Riga'
		},
		'ru': {
			'language': 'ru',
			'value': 'улица в Риге'
		}
	}
}, {
	'cat':
	'Ielas Jūrmalā',
	'dep':
	'0',
	'name':
	'Jūrmalas ielas',
	'claims': [{
		'prop': 'P31',
		'val': 'Q79007'
	}, {
		'prop': 'P17',
		'val': 'Q211'
	}, {
		'prop': 'P131',
		'val': 'Q178382'
	}],
	'descs': {
		'lv': {
			'language': 'lv',
			'value': 'iela Jūrmalā'
		},
		'en': {
			'language': 'en',
			'value': 'street in Jūrmala'
		}
	}
}, {
	'cat':
	'Ielas Jelgavā',
	'dep':
	'0',
	'name':
	'Ielas Jelgavā',
	'claims': [{
		'prop': 'P31',
		'val': 'Q79007'
	}, {
		'prop': 'P17',
		'val': 'Q211'
	}, {
		'prop': 'P131',
		'val': 'Q179830'
	}],
	'descs': {
		'lv': {
			'language': 'lv',
			'value': 'iela Jelgavā'
		},
		'en': {
			'language': 'en',
			'value': 'street in Jelgava'
		}
	}
}, {
	'cat':
	'Latvijas upes pēc novada',
	'dep':
	'2',
	'name':
	'Latvijas upes',
	'claims': [{
		'prop': 'P31',
		'val': 'Q4022'
	}, {
		'prop': 'P17',
		'val': 'Q211'
	}],
	'descs': {
		'lv': {
			'language': 'lv',
			'value': 'upe Latvijā'
		},
		'en': {
			'language': 'en',
			'value': 'river in Latvia'
		}
	}
}, {
	'cat':
	'Skolas Rīgā',
	'dep':
	'0',
	'name':
	'Rīgas skolas',
	'claims': [{
		'prop': 'P31',
		'val': 'Q3914'
	}, {
		'prop': 'P17',
		'val': 'Q211'
	}, {
		'prop': 'P131',
		'val': 'Q1773'
	}],
	'descs': {
		'lv': {
			'language': 'lv',
			'value': 'skola Rīgā'
		},
		'en': {
			'language': 'en',
			'value': 'school in Riga'
		}
	}
}, {
	'cat':
	'Latvijas ciemi',
	'dep':
	'0',
	'name':
	'Latvijas ciemi',
	'claims': [{
		'prop': 'P31',
		'val': 'Q532'
	}, {
		'prop': 'P17',
		'val': 'Q211'
	}],
	'descs': {}
}, {
	'cat':
	'Dziesmas latviešu valodā',
	'dep':
	'0',
	'name':
	'Dziesmas latviešu valodā',
	'claims': [{
		'prop': 'P31',
		'val': 'Q7366'
	}, {
		'prop': 'P407',
		'val': 'Q9078'
	}],
	'descs': {}
}, {
	'cat':
	'Filmas latviešu valodā',
	'dep':
	'0',
	'name':
	'Filmas latviešu valodā',
	'claims': [{
		'prop': 'P31',
		'val': 'Q11424'
	}, {
		'prop': 'P407',
		'val': 'Q9078'
	}, {
		'prop': 'P17',
		'val': 'Q211'
	}],
	'descs': {}
}]


def main():
	for one in jsonobj:
		pywikibot.output(one['name'])
		lvwikiarticles = get_from_petscan(one['cat'], one['dep'])
		clms = one['claims']
		descs = one['descs']

		for candidate in lvwikiarticles:
			one_item(candidate, clms, descs)


#
main()
