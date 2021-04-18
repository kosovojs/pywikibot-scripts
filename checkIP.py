import pywikibot, os, ipaddress
import toolforge
from datetime import timedelta, datetime

conn = toolforge.connect('lvwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__meta_p')
cursor1 = connLabs.cursor()

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection = conn):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = connection.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()
	
	return rows
#

def get_last_run():
	query = "select lastupd from logtable where job='ip'"
	query_res = run_query(query,connLabs)
	
	return encode_if_necessary(query_res[0][0])
#
def set_last_run(timestamp):
	query = "UPDATE `logtable` SET lastupd=%s where job='ip'"
	
	timeasUTC = "{0:%Y%m%d%H%M%S}".format(timestamp)
	cursor1.execute(query, (timeasUTC))
	connLabs.commit()
#

site = pywikibot.Site("lv", "wikipedia")
site.login(sysop=True)
site.get_tokens('edit')

#ouarry = Quarry()

SQLMAIN = """select rc_this_oldid, rc_title, rc_namespace, comment_text
from recentchanges rc
join comment c on rc.rc_comment_id=c.comment_id
where rc_timestamp>{} and rc_type=0 and comment_text like "Novērsu izmaiņas%"
"""

def get_articles():
	lastRun = "{0:%Y%m%d%H%M%S}".format(get_last_run())
	query_res = run_query(SQLMAIN.format(lastRun),conn)
	
	return query_res#[encode_if_necessary(f[0]) for f in query_res]
#
thelist = get_articles()#ouarry.get('32687')[0]


def putNotif(message):
	r = pywikibot.data.api.Request(site=site, action='edit', format='json',
										title='Vikipēdija:Administratoru ziņojumu dēlis', section='new', sectiontitle='IP adrešu labojumi', text=message,token=site.tokens['edit'], summary='IP adrešu labojumi').submit()#, summary='tests3'
#

parsed = {}

toreport = []

for one in thelist:
	one = [encode_if_necessary(f) for f in one]
	editid,title,ns, comment = one
	
	if 'WP:HG' in comment: continue
	try:
		_,comment = comment.split('versiju, ko saglabāja ')
	except ValueError:
		pywikibot.output(comment)
	try:
		ip = ipaddress.ip_address(comment)
		toreport.append([editid,title,ns])
	except ValueError:
		continue
#

if len(toreport)>0:
	formatted = '* [[Special:Diff/{0}|{0}]] ([[{{{{ns:{2}}}}}:{1}]])'
	thetext = 'Šajos labojumos tikušas saglabātas IP adrešu saglabātās versijas. Lūdzu pārbaudiet!\n{}\n--~~~~'.format('\n'.join([formatted.format(f[0],f[1].replace('_',' '),f[2]) for f in toreport]))
	putNotif(thetext)
set_last_run(datetime.utcnow())