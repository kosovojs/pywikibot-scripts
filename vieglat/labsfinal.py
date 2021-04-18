import pywikibot, re

fileeopen = open('dsfsdfsdfsdfsdfsdfsdfsdfsdfsdfsd.txt','r', encoding='utf-8').read()

site = pywikibot.Site("wikidata", "wikidata")
articletitle = 'User:Edgars2007/IAAF'
saglapa = pywikibot.Page(site,articletitle)

saglapa.text = fileeopen

saglapa.save(summary='upd', botflag=False, minor=False)