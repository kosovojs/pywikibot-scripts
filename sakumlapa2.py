#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import time
import pywikibot

site = pywikibot.Site("lv", "wikipedia")

db = cnx1 = MySQLdb.connect(host="lvwiki.analytics.db.svc.eqiad.wmflabs", db="lvwiki_p", read_default_file="~/replica.my.cnf", charset='utf8')
cur = db.cursor()
text = ''

cur.execute("select rev_user_text from revision limit 15")
for row in cur.fetchall():
	pywikibot.output(row)
#

report_pageE = pywikibot.Page(site,'User:Edgars2007/Cron')
report_pageE.text = text
report_pageE.save(summary=u'bots: atjauninâts')