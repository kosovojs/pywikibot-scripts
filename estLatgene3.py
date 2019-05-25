import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone
from customFuncs import get_quarry

cached = False
cachedDB = False

#os.chdir(r'projects/estlat')

conn = toolforge.connect('enwiki_p','analytics')
#connLabs = toolforge.connect_tools('s53143__estlat_p')
#cursor1 = connLabs.cursor()

null = ''

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")
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

SQL_ruwiki = """select count(l.ll_lang) as langs, p.page_title, (select m2.ll_title from langlinks m2 where m2.ll_from=l.ll_from and m2.ll_lang="lv")  as en, (select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd
from langlinks l
join page p on p.page_id=l.ll_from
group by l.ll_from
#having count(l.ll_lang)>20
order by count(l.ll_lang) desc
limit 15000;"""


def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

def ruwiki_query(countryname,country,language):
	printInfo('ru',countryname,country,language)
	if cached:
		return {}
	else:
		query_res = run_query(SQL_ruwiki.format(country,language),toolforge.connect('ltgwiki_p','analytics'))
		result_json = [encode_all_items(f) for f in query_res]
		frwikidata = {}
		
		for line in result_json:
			iws,fr,en,wd = line
			
			if en is None:
				frwikidata.update({wd:[iws,['ru',fr.replace('_',' ')]]})
			else:
				frwikidata.update({wd:[iws,['en',en]]})
		
		final2 = sort_list(frwikidata)
		saveToDB(final2,language,countryname,'ltg')
		return frwikidata
#
sql_update = 'UPDATE `lists` SET jsondata=%s, last_upd=%s where wiki=%s and name=%s and list_type=%s and source=%s'

def saveToDB(jsonData,wiki,countryname,source):
	curr_time = utc_to_local(datetime.utcnow())
	currTime = "{0:%Y%m%d%H%M%S}".format(curr_time)
	
	#jsondata=%s, last_upd=%s where wiki=%s and name=%s and list_type=%s'
	if cachedDB:
		with open('cats datggfgdfga2{}{}.txt'.format(wiki,source), "w", encoding='utf-8') as fileW:
			fileW.write(str(jsonData))
	else:
		connLabs = toolforge.connect_tools('s53143__estlat_p')
		cursor1 = connLabs.cursor()
		cursor1.execute(sql_update, (str(json.dumps(jsonData)),currTime,wiki,countryname,"list",source))
		connLabs.commit()
		connLabs.close()
#
def printInfo(FUNC,countryname,country,language):
	pywikibot.output("FUNC: {}\tcountryname: {}\tcountry: {}\tlanguage: {}".format(FUNC,countryname,country,language))
	
def sort_list(thelist):
	final = []
	
	for one in thelist:
		thisdata = thelist[one]
		final.append([one,thisdata[0],thisdata[1]])
	
	final2 = sorted(final, key=lambda x: -int(x[1]))
	
	return final2

def main():
	languages = ['lv']
	countries = {'lv':{'en':'Latvia','fr':'Lettonie','ru':'Латвия'}}
	
	for country in countries:#kuras valsts saraksts tiek veidots
		if country=='et': continue#Latvija ir novembrī, to vēlāk
		
		countryname = 'Latvia'
		
		countrydata = countries[country]
		
		for wiki in languages:#kurai wiki šis saraksts domāts
			ruwiki_query(countryname,countrydata['ru'],wiki)
			
	#connLabs.close()
	conn.close()
	pywikibot.output('done')
	
#

#
main()