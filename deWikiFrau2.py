import pywikibot, re, os, time, sys, json, operator
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

conn = toolforge.connect('dewiki_p','analytics')

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
SQL_main = """select count(l.ll_lang), p.page_title, 
	(select pp.pp_value from page_props pp where pp.pp_page=p.page_id and pp_propname='wikibase_item') as wd,
    (SELECT GROUP_CONCAT(cl_to SEPARATOR '|') FROM categorylinks cl where cl.cl_from=p.page_id and  cl_to like "Geboren_%") as cats
from langlinks l
join page p on p.page_id=l.ll_from
and p.page_namespace=0 and not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
	and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
               										and cla.cl_to="Frau"
               )
group by l.ll_from
order by count(l.ll_lang) desc
limit 90000;"""

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

sql_insert = 'INSERT INTO `entries` (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

bigm = {}

def sort_order(themas):
	toadd = {}
	toadd1 = {}
	for one in themas:
		if '. gs pme' in one:
			toadd.update({one:(int((one.replace('. gs pme','')))+1)*100*-1})
		elif '. gs' in one and one.replace('. gs','').isdigit():
			toadd.update({one:(int(one.replace('. gs',''))-1)*100})
		elif one.replace('s','').isdigit():
			toadd.update({one:int(one.replace('s',''))})
		else:
			toadd1.update({one:one})
	
	sorted_d = sorted(toadd.items(), key=operator.itemgetter(1))
	sorted_d1 = sorted(toadd1.items(), key=operator.itemgetter(1))
	#pywikibot.output(sorted_d)
	#pywikibot.output(sorted_d1)
	
	return sorted_d[::-1]+sorted_d1
#
def centuryFromYear(text,year):
	try:
		year = int(year)
		if year % 100 == 0:
			return (year % 100)
		else:
			return (year % 100) + 1
	except:
		return 'DIDNOT'
	#	print(text)
	#	year = 0
#
def parse_dob(text):
	toret = ''
	
	#if isinstance(text, int)
	#if len(text)==4:
	#	toret = text[:3]
	
	if re.match('^\d+$',text):
		intdob = int(text)
		if intdob>1800:#pēdējās desmitgades sadalīt uz pusēm
			toret = text[:-1]+'0s'
		else:
			toret = str(centuryFromYear(text,text[:-2]))+'. gs'
	reg1 = re.search('^im_(\d+)\._Jahrhundert$',text)
	
	if reg1:
		toret = reg1.group(1)+'. gs'
		
	reg1 = re.search('^im_(\d+)\._Jahrhundert_v\._Chr\.$',text)
	
	if reg1:
		intdob = int(reg1.group(1))
		
		if intdob<51:
			toret = reg1.group(1)+'. gs pme'
		else:
			toret = 'pme'
			
	reg1 = re.search('^(\d+)_v\._Chr\.$',text)
	
	if reg1:
		intdob = centuryFromYear(text,reg1.group(1))
		#print(intdob)
		if intdob<51:
			toret = str(intdob)+'. gs pme'
		else:
			toret = 'pme'
	
	if toret=='':
		return False
	
	return toret
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
	
	result_json = ['\t'.join(map(str,encode_all_items(f))) for f in query_res]
	curr_time = utc_to_local(datetime.utcnow())
	dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
	pywikibot.output(dateforq1)
	
	with open('quarry-27936-women-2.txt','w', encoding='utf-8') as fileOpen:
		fileOpen.write('\n'.join(result_json))
	pywikibot.output('done')
	#return result_json
#

getData()