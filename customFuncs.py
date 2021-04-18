#!/usr/bin/env python3
# -*- coding: utf-8  -*-
import re, pywikibot, json, requests
import urllib.parse as urlparse
#customFuncs

null = ''
#
def basic_petscan(id):
	#http://petscan.wmflabs.org/?psid=157563&format=json
	payload = {
		'psid': id,
		'format': 'json'
	}

	r = requests.get('http://petscan.wmflabs.org/?', params=payload)
	r.encoding = 'utf-8'
	json_data = eval(r.text)
	
	#items = [f["item"]["value"].replace('http://www.wikidata.org/entity/','') for f in json_data['results']['bindings']]
	
	return json_data['*'][0]['a']['*']

#
def basic_sparql(query):
	
	payload = {
		'query': query,
		'format': 'json'
	}

	r = requests.get('https://query.wikidata.org/bigdata/namespace/wdq/sparql?', params=payload)
	r.encoding = 'utf-8'
	json_data = eval(r.text)
	
	#items = [f["item"]["value"].replace('http://www.wikidata.org/entity/','') for f in json_data['results']['bindings']]
	
	return json_data['results']['bindings']

def get_quarry_run(page_id):
	url = 'https://quarry.wmflabs.org/query/{}'.format(page_id)
	res = requests.get(url)
	pagetext = res.text
	
	reg = '"qrun_id": (\d+)'
	
	qid = re.search(reg, pagetext)
	
	if qid:
		return qid.group(1)
#
def get_quarry(page_id,listing='0'):
	url = 'https://quarry.wmflabs.org/query/{}/result/latest/{}/json'.format(page_id,listing)
	res = requests.get(url)
	data = eval(res.text)
	
	return data["rows"]
	'''
	#kā sarakstu - json failu kversiju rez - [0,1,2,3]
	url = 'https://quarry.wmflabs.org/query/{}'.format(page_id)
	res = requests.get(url)
	pagetext = res.text
	
	reg = '"qrun_id": (\d+)'
	
	qid = re.search(reg, pagetext)
	
	if qid:
		url2 = "https://quarry.wmflabs.org/run/{}/output/{}/json".format(qid.group(1),listing)
	
		url23= requests.get(url2)#.read()
		#print('here1fsdfsd')
		#pywikibot.output(url2.text)

		data = json.loads(url23.text)
		#print('here1fsdfssfsdfd')
		return data["rows"]
	'''
#
def hasprop(prop):
	
	SPARQL = "select ?item {{ ?item p:{} [] . }}".format(prop)
	#SELECT ?item { ?item p:P961 [] . }
	
	payload = {
		'query': SPARQL,
		'format': 'json'
	}

	r = requests.get('https://query.wikidata.org/bigdata/namespace/wdq/sparql?', params=payload)
	r.encoding = 'utf-8'
	json_data = json.loads(r.text)
	
	items = [f["item"]["value"].replace('http://www.wikidata.org/entity/','') for f in json_data['results']['bindings']]
	
	return items
#
def haspropVAL(prop):
	
	SPARQL = "SELECT ?item ?value {{ ?item p:{prop} [ ps:{prop} ?value ] . }}".format(prop=prop)
	#SELECT ?item ?value { ?item p:P961 [ ps:P961 ?value ] . }
	
	payload = {
		'query': SPARQL,
		'format': 'json'
	}

	r = requests.get('https://query.wikidata.org/bigdata/namespace/wdq/sparql?', params=payload)
	r.encoding = 'utf-8'
	json_data = json.loads(r.text)
	
	itemdata = {}
	
	for item in json_data['results']['bindings']:
		wdit = item["item"]["value"].replace('http://www.wikidata.org/entity/','')
		wdval =item["value"]["value"]
		
		if wdit in itemdata:
			if wdval not in itemdata[wdit]:
				itemdata[wdit].append(wdval)
		else:
			itemdata[wdit] = [wdval]
	
	return itemdata
#
def haspropWiki(prop,lang):
	
	SPARQL = "SELECT ?sitelink ?value {{ ?item p:{prop} [ ps:{prop} ?value ] . ?sitelink schema:about ?item; schema:isPartOf <https://{lang}.wikipedia.org/> . }}".format(prop=prop,lang=lang)
	#SELECT ?sitelink ?value { ?item p:P2697 [ ps:P2697 ?value ] . ?sitelink schema:about ?item; schema:isPartOf <https://lv.wikipedia.org/> . }
	
	payload = {
		'query': SPARQL,
		'format': 'json'
	}
	
	r = requests.get('https://query.wikidata.org/bigdata/namespace/wdq/sparql?', params=payload)
	r.encoding = 'utf-8'
	json_data = json.loads(r.text)
	
	itemdata = {}
	
	makeurlstring = 'https://{}.wikipedia.org/wiki/'.format(lang)
	
	for item in json_data['results']['bindings']:
		wdit = urlparse.unquote(item["sitelink"]["value"].replace(makeurlstring,''))
		wdval = item["value"]["value"]
		
		if wdit in itemdata:
			if wdval not in itemdata[wdit]:
				itemdata[wdit].append(wdval)
		else:
			itemdata[wdit] = [wdval]
	
	return itemdata
#
def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#
def pagename(bg):
	bg = re.sub('\s*(\([^\(]+)$','',bg)
	
	return bg
#
def sanityvalue(value):
	value = re.sub('<!--.*?-->', '',value)#remove comments
	value = re.sub('<ref([^>]+)\/>', '',value)#remove self-closing reference tags
	value = re.sub('<ref((?!<\/ref>).)*<\/ref>', '',value)#remove references
	value = re.sub('<ref([^>]+)>', '',value)#remove reference tags
	
	return value
#