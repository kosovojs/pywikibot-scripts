import os, pywikibot
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
	query = "select lastupd from logtable where job='uzlabosana'"
	query_res = run_query(query,connLabs)
	
	return encode_if_necessary(query_res[0][0])
#
def set_last_run(timestamp):
	query = "UPDATE `logtable` SET lastupd=%s where job='uzlabosana'"
	
	timeasUTC = "{0:%Y%m%d%H%M%S}".format(timestamp)
	cursor1.execute(query, (timeasUTC))
	connLabs.commit()
#

site = pywikibot.Site("lv", "wikipedia")
site.login(sysop=True)
site.get_tokens('edit')

#ouarry = Quarry()

SQLMAIN = """select page_namespace, page_title, rc_timestamp, actor_name as rc_user_text, rc_title, rc_this_oldid, rc_params
from recentchanges
join page on rc_cur_id=page_id
join actor on rc_actor=actor_id
where rc_type=6 and rc_timestamp>{} and page_namespace=0 and rc_params like '%"added";b:0%'
	and actor_name not in (select distinct user_name from user_groups join user on user_id=ug_user)
order by rc_timestamp desc
"""

def get_articles():
	lastRun = "{0:%Y%m%d%H%M%S}".format(get_last_run())
	query_res = run_query(SQLMAIN.format(lastRun),conn)
	
	return query_res#[encode_if_necessary(f[0]) for f in query_res]
#
thelist = get_articles()#ouarry.get('32687')[0]


def putNotif(message):
	r = pywikibot.data.api.Request(site=site, action='edit', format='json',
										title='Vikipēdija:Administratoru ziņojumu dēlis', section='new', sectiontitle='Jaunu dalībnieku labojumi', text=message,token=site.tokens['edit'], summary='Jaunu dalībnieku labojumi').submit()#, summary='tests3'
#


allcats = ['Lapas, kas izvirzītas dzēšanai', 'Raksti, kurus ierosināts apvienot', 'Raksti, kuru faktuālais akurātums ir ticis apšaubīts', 'Raksti, kurus ierosināts sadalīt', 'Raksti, kuros informācija ir novecojusi', 'Raksti, kuriem trūkst atsauču', 'Raksti, kurus ierosināts sadalīt', 'Raksti, kuros nav ievēroti īpašvārdu atveidošanas principi', 'Autobiogrāfiski raksti', 'Iespējami autortiesību pārkāpumi', 'Iespējami autortiesību pārkāpumi', 'Raksti, kas jāuzlabo ekspertam', 'Raksti, kuros nav ievērots enciklopēdisks stils', 'Raksti, kam vajadzīga infokaste', 'Izolētie raksti', 'Raksti, kas jāuzlabo', 'Raksti, kas jāpārraksta', 'Raksti bez ievada', 'Nekategorizētie raksti', 'Raksti, kuros iespējams interešu konflikts', 'Raksti, kuriem ir problēmas ar informācijas izklāstu', 'Raksti, kuriem trūkst atsauču', 'Nepilnīgi raksti', 'Raksti, kuru temata nozīmīgums tiek apšaubīts', 'Raksti, kuriem trūkst atsauču', 'Veidnes, kam nepieciešama dokumentācija', 'Raksti, kuros nepieciešams papildināt nodaļu saturu', 'Raksti, kam jāuzlabo noformējums', 'Novecojuši sporta klubu sastāvi', 'Raksti, kuriem trūkst atsauču', 'Raksti, kuros nav ievēroti pareizrakstības principi', 'Iespējami autortiesību pārkāpumi', 'Raksti, kuru neitralitāte ir apšaubāma', 'Raksti, kurus ierosināts sadalīt', 'Raksti, kam jāsadala teksts', 'Raksti, kas jāpārraksta saistītā tekstā', 'Slikti iztulkoti raksti', 'Raksti, kuros nav saišu uz citu valodu Vikipēdijām', 'Raksti, kam vajadzīgs teksts', 'Raksti, kam jāpievieno informācija no citiem avotiem', 'Raksti, kuros nav vikisaišu', 'Raksti svešvalodā']#, 'Visi_Vikipēdijas_uzlabojamie_raksti'

allcats = [f.replace(' ','_') for f in allcats]

parsed = {}

toreport = []

for one in thelist:
	one = [encode_if_necessary(f) for f in one]
	page_namespace, page_title, rc_timestamp, rc_user_text, rc_title, rc_this_oldid, rc_params = one
	
	if rc_this_oldid in parsed:
		parsed[rc_this_oldid].append(one)
	else:
		parsed[rc_this_oldid] = [one]
#
for edit in parsed:
	data = parsed[edit]
	dfdf = [f for f in data if f[4] in allcats]
	if len(dfdf)<1: continue
	
	toreport.append(dfdf)
#

if len(toreport)>0:
	formatted = '* [[Special:Diff/{0}|{0}]] ([[{1}]]): {{{{no ping|{2}}}}}'
	thetext = 'Šajos labojumos tikušas izņemtas uzlabošanas veidnes. Lūdzu pārbaudiet!\n{}\n--~~~~'.format('\n'.join([formatted.format(f[0][5],f[0][1].replace('_',' '),f[0][3]) for f in toreport]))
	putNotif(thetext)
set_last_run(datetime.utcnow())