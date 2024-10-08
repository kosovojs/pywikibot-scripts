import re, pywikibot
import toolforge

site = pywikibot.Site('lv', "wikipedia")
conn = toolforge.connect('lvwiki_p')

SQL = """SELECT page_title FROM page
LEFT JOIN (pagelinks pl join linktarget lt on lt.lt_id=pl.pl_target_id and lt_namespace=0) ON pl_from = page_id
WHERE lt_namespace IS NULL and page_is_redirect=0 and page_namespace=0
and not exists (select * from categorylinks c566 where
                   				page_id = c566.cl_from AND c566.cl_to="Raksti,_kuros_nav_vikisaišu")
"""

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query():
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(SQL)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows
#
text1 = [encode_if_necessary(f[0]) for f in run_query()]

tpltext = "{{vikisaites+}}"

reg = re.compile(r'{{(template:|veidne:)?vikisaites\+[\|\}]', re.I)#re.compile(r'\{\{(?:veidne:|template:)(izolēts_?raksts|orphan)[\|\}]', re.I)

def main():
	for article in text1:
		pywikibot.output('\t'+article)
		page = pywikibot.Page(site,article)
		try:
			oldtxt = page.get(get_redirect=True)
		except pywikibot.exceptions.NoPage:
			continue

		searchtl = re.search(reg, oldtxt)

		if searchtl:
			print('already has template')
			continue

		newtxt = tpltext + "\n"+oldtxt
		page.text = newtxt

		page.save(comment='Bots: pievienota {{vikisaites+}} veidne. [[Dalībnieka diskusija:Edgars2007|Kļūda?]]', botflag=True, minor=False)
#
main()
