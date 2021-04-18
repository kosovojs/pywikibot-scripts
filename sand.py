#!/usr/bin/python
# -*- coding: utf-8 -*-
import pywikibot
import re

site = pywikibot.Site("lv", "wikipedia")
editsummary = u"Robots: smilšu kastes tīrīšana"

def mainSandbox(site):
	content = u"<!-- LŪGUMS NEDZĒST ŠO RINDIŅU ♦♦♦ PLEASE, DON'T DELETE THIS LINE -->{{Smilšu kaste}}<!-- LŪGUMS NEDZĒST ŠO RINDIŅU ♦♦♦ PLEASE, DON'T DELETE THIS LINE -->"
	article = u"Vikipēdija:Smilšu kaste"
	page = pywikibot.Page(site,article)
	page.text = content
	page.save(editsummary)

def otherSandboxes(site):
	sandboxes = [u'Vikipēdija:Pamācība (Noformēšana)/smilšu kaste',
				u'Vikipēdija:Pamācība (Vikipēdijas saites)/smilšu kaste',
				u'Vikipēdija:Pamācība (Ārējās saites)/smilšu kaste',
				u'Vikipēdija:Pamācība (Labošana)/smilšu kaste',
				u'Vikipēdija:Pamācība (Saites uz saistītiem projektiem)/smilšu kaste'
				]
	for sandbox in sandboxes:
		pageToSave = pywikibot.Page(site,sandbox)
		pageToSave.text = ''
		pageToSave.save(editsummary)

def main():
	mainSandbox(site)
	otherSandboxes(site)

if __name__ == "__main__":
    main()
