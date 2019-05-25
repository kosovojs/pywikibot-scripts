#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pywikibot, requests, re, json, urllib.parse
from urllib import parse

lvwiki = pywikibot.Site("lv", "wikipedia")

############################# IMDb top 250 page source
url = "http://www.imdb.com/chart/top"
url2= requests.get(url)
top250_source = url2.text
soup_object = BeautifulSoup(top250_source, "html.parser")

#######################################################################################

###Helper functions

def pagename(bg):
	bg = re.sub('\s*(\([^\(]+)$','',bg)
	
	return bg
	
def createnos(mydict,imbd):
	row = ''
	dtaa = mydict[imbd]
	lv = dtaa[1]
	en = dtaa[0]
	
	if lv!='':
		pg = pagename(lv)
		if lv==pg:
		
			row = '"[[{}]]"'.format(lv)
		else:
			row = '"[[{}|{}]]"'.format(lv,pg)
	elif en!='':
		pg = pagename(en)
		if en==pg:
		
			row = "''[[{}]]''".format(en)
		else:
			row = "''[[{}|{}]]''".format(en,pg)
			
	if '(film)' in row:
		row = row.replace('(film)','(filma)')
		
	return row

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def oneBatch(titles,mydict):
	toquery = '" "'.join(titles)
	itemlist = {}
	
	QUERY = """SELECT ?ids ?item ?articleLV ?articleEN WHERE {
  ?item wdt:P345 ?ids .
  values ?ids { "%s" }
    OPTIONAL { ?articleLV schema:about ?item ; schema:isPartOf <https://lv.wikipedia.org/> }
    OPTIONAL { ?articleEN schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> }
	}""" % toquery
	
	#pywikibot.output(QUERY)
	
	query2 = urllib.parse.quote(QUERY)
	
	url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}&format=json".format(query2)
	url2= requests.get(url)
	url2.encoding = 'utf-8'
	
	json_data = json.loads(url2.text)
	
	#{'item': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q132351'}, 'articleEN': {'type': 'uri', 'value': 'https://en.wikipedia.org/wiki/The%20Usual%20Suspects'}, 'articleLV': {'type': 'uri', 'value': 'https://lv.wikipedia.org/wiki/Parastie%20aizdom%C4%81s%20turamie'}}
	itemlist = {data['ids']['value']:[parse.unquote(data['articleEN']['value'].replace('https://en.wikipedia.org/wiki/','').replace('_',' ')) if 'articleEN' in data else '',
										parse.unquote(data['articleLV']['value'].replace('https://lv.wikipedia.org/wiki/','').replace('_',' ')) if 'articleLV' in data else '']
				for data in json_data['results']['bindings']
				}
				
	return itemlist

def getids():
	soup = soup_object
	
	arr = []

	table = soup.find('table',{'data-caller-name':'chart-top250movie'})
	tbody = table.find('tbody')
	#trs = table.find_all('tr')

	for row in tbody.find_all('tr'):
		tds = row.find_all('td')
		#pywikibot.output(tds)
	
		secdata = tds[1]
		
		title = secdata.a.text
		id = secdata.a['href']
		year = secdata.span.text
		
		regex = "\/title\/(tt\d+)\/"
		idM = re.search(regex,id)
		newid = idM.group(1)
		
		arr.append(newid)
		
	return arr

#######################################################################################
def dostufff(mydict):
	
	counter = 1
	
	soup = soup_object
	
	arr = []

	table = soup.find('table',{'data-caller-name':'chart-top250movie'})
	tbody = table.find('tbody')
	#trs = table.find_all('tr')

	for row in tbody.find_all('tr'):
		tds = row.find_all('td')
		#pywikibot.output(tds)
	
		votes = tds[0]
		votes2 = votes.find('span',{'name':'ir'})
		votes2 = votes2['data-value']
		
		votes2 = float(votes2)
		votes2 = '{:.3f}'.format(votes2)
		votes2 = str(votes2).replace('.',',')
		
		
		secdata = tds[1]
		votes3 = str.strip(tds[2].text)
		
		title = secdata.a.text
		id = secdata.a['href']
		year = secdata.span.text
		
		regex = "\/title\/(tt\d+)\/"
		idM = re.search(regex,id)
		newid = idM.group(1)
		
		yearregex = "\((\d+)\)"
		yearM = re.search(yearregex,year)
		year = yearM.group(1)
		
		#pywikibot.output(votes3)
		#pywikibot.output(votes2)
		#pywikibot.output(title)
		#pywikibot.output(newid)
		#pywikibot.output(year)
		
		title2 = createnos(mydict,newid)#title#createnos(newid)
		
		finalrow = '|-\n| %s\n| %s || %s || %s' % (counter,title2,year,votes2)
		#pywikibot.output(finalrow)
		arr.append(finalrow)
		
		counter = counter+1
		
		
	output = '{| class="wikitable sortable"\n|-\n! scope="col"| {{piezīme|V|Vieta}} !! style="width:300px;"| Filma !! Gads !! Vērtējums\n'+'\n'.join(arr)+'\n|}\n'
	
	return output

def doreplace(text,pretext,header,footer):
	newtext = re.sub(header + '.*' + footer, header + pretext + footer, text, flags=re.DOTALL)
	#pywikibot.output(newtext)
	
	return newtext
#

def main():
	#first, get ID list
	top250ids = getids()
	
	#get sparql data
	mydict = {}
	for group in chunker(top250ids,20):
		thisres = False
		thisres = oneBatch(group,mydict)
		mydict.update(thisres)
		
	pywikibot.output('Got {} results from SPARQL query'.format(len(mydict)))
	
	file1 = open('imdbtop250-sparqlres.txt', "w", encoding='utf-8')
	file1.write(str(mydict))
	
	
	out = dostufff(mydict)
	
	list_header = '<!-- LIST START -->'
	list_footer = '<!-- LIST END -->'
	
	lvpage = pywikibot.Page(lvwiki,"IMDb Top 250")
	text = lvpage.get()
	newtext = doreplace(text,'\n'+out,list_header,list_footer)
	lvpage.text = newtext
	lvpage.save(summary='atjaunināts saraksts', botflag=False, minor=False)
	
	file = open('imdb.txt', "w", encoding='utf-8')
	file.write(out)

if __name__ == "__main__":
	main()