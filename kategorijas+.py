import pywikibot, re, os
import toolforge
from nobots import deny_bots

site = pywikibot.Site('lv', "wikipedia")
conn = toolforge.connect('lvwiki_p','analytics')

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#
SQL_main = """SELECT p.page_title, GROUP_CONCAT(cl_to SEPARATOR '|') as cats
FROM page p
INNER JOIN categorylinks cl ON cl.cl_from = p.page_id
WHERE p.page_namespace=0 and p.page_is_redirect=0 and p.page_id not in (select cl_from
							from categorylinks
							where cl_to="Nekategorizētie_raksti")
group by p.page_id;"""

SQL_hidden = """SELECT p2.page_title
from page p2
JOIN page_props pp ON pp.pp_page = p2.page_id AND pp.pp_propname = 'hiddencat'
where p2.page_namespace = 14;"""

SQL_no_cats = """select page_title
from page
where page_is_redirect=0 and page_namespace=0 and not exists (select cl_from from categorylinks cl where cl.cl_from = page_id limit 1)
"""


hidden = run_query(SQL_hidden)
hidden = [encode_if_necessary(f[0]) for f in hidden]


no_cats = run_query(SQL_no_cats)
no_cats = [encode_if_necessary(f[0]) for f in no_cats]

badcats = [
	'Visi_Vikipēdijas_aizmetņi',
	'Visi_Vikipēdijas_uzlabojamie_raksti',
	'Sevišķi_īsi_raksti',
	'Dzēšanai_izvirzītās_lapas'
]

cattocheck = []

cattocheck.extend(badcats)
cattocheck.extend(hidden)
#cattocheck.extend(redlinked)

badarticles = []
badarticles.extend(no_cats)

def removecats(category):
	reg = '(\d{1,4}\._gadā_(dzimušie|mirušie)|Nepabeigti_raksti)'#reg = '\d{1,4}\._gadā_(dzimušie|mirušie)'
	res = re.search(reg, category)#res = re.match(reg, category)
	
	if res:
		return True

main_list = run_query(SQL_main)


for article in main_list:
	article = [encode_if_necessary(f) for f in article]
	art, cats = article
	cats2 = cats.split('|')
	if 'dzimušie' in cats or 'mirušie' in cats or 'Nepabeigti' in cats:
		#pywikibot.output(cats2)
		cats2 = [cat for cat in cats2 if not removecats(cat)]
		#pywikibot.output(cats2)
	
	#pywikibot.output(cats)
	
	catdiff = set(cats2) - set(cattocheck)
	
	if len(catdiff)==0:
		badarticles.append(art)
#
with open('badarticles without real cats-2.txt', "w", encoding='utf-8') as filsesave:
	filsesave.write(str(badarticles))

tpltext = "{{kategorijas+}}"

reg = re.compile(r'{{(template:|veidne:)?kat(egorijas)\+[\|\}]', re.I)#re.compile(r'\{\{(?:veidne:|template:)(izolēts_?raksts|orphan)[\|\}]', re.I)

def main():
	for article1 in badarticles:
		if article1 in ['Sākumlapa']:
			continue
		pywikibot.output('\t'+article1)
		page = pywikibot.Page(site,article1)
		try:
			oldtxt = page.get(get_redirect=True)
		except pywikibot.exceptions.NoPage:
			continue
		
		if deny_bots(oldtxt,'kategorijas+'): continue
		
		searchtl = re.search(reg, oldtxt)
		
		if searchtl:
			print('already has template')
			continue
			
		newtxt = tpltext + "\n"+oldtxt
		page.text = newtxt
		
		page.save(comment='Bots: pievienota {{kategorijas+}} veidne. [[Dalībnieka diskusija:Edgars2007|Kļūda?]]', botflag=True, minor=False)
#
main()