import re, pywikibot, sys
from datetime import datetime
import toolforge

site = pywikibot.Site('lv', "wikipedia")

currentMonth = str(datetime.now().month)
currentY = datetime.now().year
conn = toolforge.connect('lvwiki_p')

mondict = {
	'1':'janvāris',
	'2':'februāris',
	'3':'marts',
	'4':'aprīlis',
	'5':'maijs',
	'6':'jūnijs',
	'7':'jūlijs',
	'8':'augusts',
	'9':'septembris',
	'10':'oktobris',
	'11':'novembris',
	'12':'decembris'
}

tpltext = "{{{{izolēts raksts|date={}. gada {}}}}}".format(currentY,mondict[currentMonth])

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

SQL = """SELECT disambigs.page_title, COUNT(DISTINCT links.pl_from) AS direct_links, COUNT(DISTINCT redirects.page_id) AS redirects,
	COUNT(DISTINCT links.pl_from) + COUNT(DISTINCT links_to_redirects.pl_from) AS all_backlinks
	FROM (SELECT * FROM page WHERE page_is_redirect=0 and page_namespace=0) AS disambigs
	#JOIN page AS disambigs
	#	ON disambigs.page_id = pp_page
	LEFT JOIN (SELECT * FROM pagelinks WHERE pl_from_namespace = 0) AS links
		ON links.pl_title = disambigs.page_title AND links.pl_namespace = disambigs.page_namespace
	LEFT JOIN page AS redirects
		ON redirects.page_is_redirect = 1 AND redirects.page_id = links.pl_from AND redirects.page_namespace = disambigs.page_namespace
	LEFT JOIN (SELECT * FROM pagelinks WHERE pl_from_namespace = 0) AS links_to_redirects
		ON links_to_redirects.pl_title = redirects.page_title AND links_to_redirects.pl_namespace = redirects.page_namespace
where not exists (select * from categorylinks c566 where
                  				disambigs.page_id = c566.cl_from AND c566.cl_to in ("Izolētie_raksti","Nozīmju_atdalīšana"))

GROUP BY disambigs.page_title
having all_backlinks=0
ORDER BY all_backlinks DESC, direct_links DESC, redirects, disambigs.page_title
"""

def run_query():
	try:
		cursor = conn.cursor()
		cursor.execute(SQL)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows
#

itemlist = run_query()

reg = re.compile(r'{{(template:|veidne:)?(orphan|izolēts raksts)[\|\}]', re.I)

def main():
	for article in itemlist:
		article = encode_if_necessary(article[0])
		print('\t'+article)
		page = pywikibot.Page(site,article)
		oldtxt = page.get()

		searchtl = re.search(reg, oldtxt)

		if searchtl:
			print('already has template')
			continue

		newtxt = tpltext + "\n"+oldtxt
		page.text = newtxt

		page.save(summary='Bots: pievienota {{izolēts raksts}} veidne', botflag=True, minor=False)

main()
