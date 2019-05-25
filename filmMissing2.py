import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

conn = toolforge.connect('enwiki_p','analytics')

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

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
SQL_main = """select p.page_title, count(l.ll_lang) as langs,
	(select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd,
    (SELECT GROUP_CONCAT(cl_to SEPARATOR '|') FROM categorylinks cl where cl.cl_from=p.page_id and  cl_to rlike "\\d\\d\\d\\d.+") as cats
from langlinks l
join page p on p.page_id=l.ll_from
where  l.ll_from in (select tl.tl_from from templatelinks tl where tl.tl_title="Infobox_film" and tl_namespace=10 and tl.tl_from_namespace=0)
and p.page_namespace=0 and l.ll_from not in (select m.ll_from from langlinks m where m.ll_lang="lv")
group by l.ll_from
order by count(l.ll_lang) desc
limit 8000;"""

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

sql_insert = 'INSERT INTO `entries` (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]
#
def getData():
	#for infobox in infoboxlist:
	pywikibot.output('\tde wiki women')
	#	sys.stdout.flush()
	begin = time.time()
	#result_json = []
	query_res = run_query(SQL_main)
	
	end = time.time()
	timelen = end-begin
	if timelen>30:
		pywikibot.output('{}'.format(timelen))
	
	result_json = [encode_all_items(f) for f in query_res]
	curr_time = utc_to_local(datetime.utcnow())
	dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
	pywikibot.output(dateforq1)
	
	with open('quarry-27936-women.txt','w', encoding='utf-8') as fileOpen:
		fileOpen.write(str(result_json))
	pywikibot.output('done')
	return result_json
#

catregex = '^(\d+)_films$'
def main():
	query_res = run_query(SQL_main)
	result_json = [encode_all_items(f) for f in query_res]
	
	bigm = {}
	
	for entry in result_json:
		title,iws,wd,cats = entry
		
		if title.endswith('(film_series)'): continue
		
		try:
			cats = cats.split('|')
		except:
			cats = []
		mycat = []
		
		
		for cat in cats:
			fsdf = re.search(catregex, cat)
			if fsdf:
				mycat.append(fsdf.group(1))
		
		#if len(mycat)!=1:
		#	pywikibot.output(title+'-'+str(mycat))
		mycat = mycat[0] if len(mycat)>0 else ''
		
		if mycat[:3]=='201':
			if mycat in bigm:
				bigm[mycat].append([title,iws, mycat])
			else:
				bigm[mycat] = [[title,iws, mycat]]
		else:
			if mycat=='':
				mycat_pre = ''
			else:
				mycat_pre = mycat[:3]+'0s'
			if mycat_pre in bigm:
				bigm[mycat_pre].append([title,iws, mycat])
			else:
				bigm[mycat_pre] = [[title,iws, mycat]]
	
	
	curr_time = utc_to_local(datetime.utcnow())
	dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
	#print(dateforq1)
	
	#put_db(infobox,result_json,dateforq1)
	#cursor1.execute(sql_insert, (infobox.replace('Infobox_','').replace('_',' '), 'eninfobox',str(json.dumps(result_json)),dateforq1))
	
	#pywikibot.output(SQL_main.format(newtitle))
	#pywikibot.output(result_json)
	#if not connLabs and not connLabs.open:
	connLabs = toolforge.connect_tools('s53143__mis_lists_p')
	cursor1 = connLabs.cursor()
	
	grupa = 'other1'
	infname = 'filmas'
	cursor1.execute('UPDATE `entries` SET jsondata=%s, last_upd=%s where group_name=%s and name=%s', (str(json.dumps(bigm)),dateforq1,grupa, infname))
	
	connLabs.commit()
	
	connLabs.close()
	
	
	#with open('frau21.json', "w", encoding='utf-8') as fileS1:
	#	fileS1.write(str(json.dumps(theorder)))#('var data = '+str(bigm)+';')
	
#
main()