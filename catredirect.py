import pywikibot, re
from customFuncs import get_quarry
import toolforge

site = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('lvwiki_p')

patt = '#REDIRECT \[\[\:?Kategorija:([^\]]+)\]\]'
repl = r'#REDIRECT [[:Kategorija:\1]]\n{{kat pāradresācija|Kategorija:\1}}'

SQL = """SELECT CONCAT('Kategorija:',p.page_title) FROM page p
#LEFT JOIN templatelinks t ON p.page_id = t.tl_from AND t.tl_namespace = 10 AND t.tl_title NOT IN ('Kat_pāradresācija')
Where p.page_namespace=14 and p.page_is_redirect=1
and not exists (select * from templatelinks t where p.page_id = t.tl_from AND t.tl_namespace = 10 AND t.tl_title='Kat_pāradresācija')"""

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
data = run_query()

#categories = [f[0] for f in get_quarry('3872')]

for categ in data:
	categ = [encode_if_necessary(f) for f in categ]
	page = pywikibot.Page(site,categ[0])
	wikitext = page.get(get_redirect=True)
	
	if 'kat pāradresācija' in wikitext:
		continue
	
	newtext = re.sub(patt,repl,wikitext)
	
	if newtext!=wikitext:
		page.text = newtext
		page.save(summary='kategorijas pāradresācija')