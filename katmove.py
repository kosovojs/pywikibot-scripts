import pywikibot
from scripts.category import CategoryMoveRobot
import toolforge

site = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('lvwiki_p')

SQL = """SELECT p.page_title, COUNT(cl.cl_from) AS anz
			FROM page p
			LEFT JOIN categorylinks cl ON p.page_title = cl.cl_to
			WHERE p.page_namespace = 14
			AND p.page_is_redirect = 1
			GROUP BY p.page_title
            having anz>0"""

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


def one_cat(OLDCAT):
	oldcatObject = pywikibot.Page(site,"Kategorija:{}".format(OLDCAT))

	if not oldcatObject.isRedirectPage():
		return 0
	#

	NEWCAT = oldcatObject.getRedirectTarget().title(withNamespace=False)
	#pywikibot.output(NEWCAT)

	SUMMARY = 'kategorija "{}" → "{}"'.format(OLDCAT.replace('_',' '), NEWCAT.replace('_',' '))
	q = CategoryMoveRobot(OLDCAT, NEWCAT, batch=True, comment=SUMMARY, inplace=True, delete_oldcat=False)
	q.run()
#
data = run_query()#oldcategory = ['Sanktpēterburgas_"SKA"_spēlētāji','','','']


for categ in data:
	categ = encode_if_necessary(categ[0])
	#pywikibot.output(categ)
	if categ=='': continue
	one_cat(categ)
