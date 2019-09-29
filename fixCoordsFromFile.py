from bs4 import BeautifulSoup
import pywikibot, requests, re, os, json, urllib.parse, sys
from urllib import parse
import pymysql, os
import pywikibot
from pywikibot import pagegenerators
from pywikibot.exceptions import CoordinateGlobeUnknownException

site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()

prop = 'P625'

#os.chdir(r'projects/vkFIX')

def one_item(article):
	item = pywikibot.ItemPage(repo,article[0])
	
	
	claims = item.get()['claims']
	if prop not in claims:
		return
	
		
	
	
	coord_lat = float(article[1])
	coord_long = float(article[2])
	precision = 0.00027777777777778#1/100000
	
	
	target = pywikibot.Coordinate(coord_lat, coord_long, precision=precision, globe_item='http://www.wikidata.org/entity/Q2')
	
	
	for one in claims[prop]:
		#one = pywikibot.Claim(repo, prop)
		one.changeTarget(target)
		return
		
	pywikibot.output(u'Adding %s, %s to %s' % (coord_lat,
						   coord_long,
						   item.title()))
	#try:
		#item.addClaim(newclaim)
		#importedEnWikipedia = pywikibot.Claim(repo, u'P248')
		#enWikipedia = pywikibot.ItemPage(repo, wikiitem)
		#$importedEnWikipedia.setTarget(enWikipedia)
		#newclaim.addSources([importedEnWikipedia])
	#except CoordinateGlobeUnknownException as e:
	#	pywikibot.output(u'Skipping unsupported globe: %s' % e.args)
#
file = eval(open("toWDcdffdfdfdoordsAREAfix.txt", "r", encoding='utf-8').read())

counter = 0
for one in file:
	one_item(one)
	counter += 1
	if counter % 50 == 0:
		print(counter)
		sys.stdout.flush()
#
print('done')