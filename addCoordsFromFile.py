from bs4 import BeautifulSoup
import pywikibot, requests, re, os, json, urllib.parse, sys
from urllib import parse
import pymysql
import pywikibot
from pywikibot import pagegenerators
from pywikibot.exceptions import CoordinateGlobeUnknownException

site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()

prop = 'P625'

def one_item(article):
	item = pywikibot.ItemPage(repo,article[0])
	
	
	claims = item.get().get('claims')
	if prop in claims:
		pywikibot.output(u'Item %s already contains coordinates (%s)'
				 % (item.title(), prop))
		return
	
	coord_lat = float(article[1])
	coord_long = float(article[2])
	precision = 0.00027777777777778#1/100000
	target = pywikibot.Coordinate(coord_lat, coord_long, precision=precision, globe_item='http://www.wikidata.org/entity/Q2')
	
	newclaim = pywikibot.Claim(repo, prop)
	newclaim.setTarget(target)
	pywikibot.output(u'Adding %s, %s to %s' % (coord_lat,
						   coord_long,
						   item.title()))
	try:
		item.addClaim(newclaim)
		#importedEnWikipedia = pywikibot.Claim(repo, u'P248')
		#enWikipedia = pywikibot.ItemPage(repo, wikiitem)
		#$importedEnWikipedia.setTarget(enWikipedia)
		#newclaim.addSources([importedEnWikipedia])
	except CoordinateGlobeUnknownException as e:
		pywikibot.output(u'Skipping unsupported globe: %s' % e.args)
#
file = eval(open("toWDcoordsAREA.txt", "r", encoding='utf-8').read())

counter = 0
for one in file:
	one_item(one)
	counter += 1
	if counter % 50 == 0:
		print(counter)
		sys.stdout.flush()
#
print('done')