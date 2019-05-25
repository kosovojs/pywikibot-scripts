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

def run_queryEN(query,connection = conn):
	
	return [[10,'','']]
def run_query(query,connection = conn):
	
	return [[10,'','','']]
'''
#
'''
SQL_enwiki = """select count(l.ll_lang) as langs, p.page_title, (select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd
from langlinks l
join page p on p.page_id=l.ll_from
where p.page_namespace=0 and p.page_title in (select distinct pla.page_title
		from categorylinks cla
		join page pla on cla.cl_from=pla.page_id# and cla.tl_from_
		where pla.page_namespace=1 and cla.cl_type="page" and cla.cl_to="WikiProject_{}_articles"
                                             )
		#where pla.page_namespace=1 and cla.cl_type="page" and cla.cl_to="WikiProject_Russia_articles")
and l.ll_from not in (select m.ll_from from langlinks m where m.ll_lang="{}")
#and l.ll_from not in (select m.ll_from from langlinks m where m.ll_lang="en")
group by l.ll_from
#having count(l.ll_lang)>20
order by count(l.ll_lang) desc
limit 1500;"""

SQL_frwiki = """select count(l.ll_lang) as langs, p.page_title, (select m2.ll_title from langlinks m2 where m2.ll_from=l.ll_from and m2.ll_lang="en")  as en, (select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd
from langlinks l
join page p on p.page_id=l.ll_from
and p.page_namespace=0 and not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="{}")
	and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
               										and cla.cl_to="Portail:{}/Articles_liés"
               )
group by l.ll_from
order by count(l.ll_lang) desc
limit 1500;"""

SQL_ruwiki = """select count(l.ll_lang) as langs, p.page_title, (select m2.ll_title from langlinks m2 where m2.ll_from=l.ll_from and m2.ll_lang="en")  as en, (select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd
from langlinks l
join page p on p.page_id=l.ll_from
where p.page_namespace=0 and p.page_title in (select distinct pla.page_title
		from categorylinks cla
		join page pla on cla.cl_from=pla.page_id# and cla.tl_from_
		where pla.page_namespace=1 and cla.cl_type="page" and cla.cl_to="Статьи_проекта_{}"
                                             )
		#where pla.page_namespace=1 and cla.cl_type="page" and cla.cl_to="WikiProject_Russia_articles")
and l.ll_from not in (select m.ll_from from langlinks m where m.ll_lang="{}")
#and l.ll_from not in (select m.ll_from from langlinks m where m.ll_lang="en")
group by l.ll_from
#having count(l.ll_lang)>20
order by count(l.ll_lang) desc
limit 1500;"""


def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

def enwiki_query(countryname,language,country):
	pywikibot.output('enwiki' + '\t'.join([countryname,language,country]))
	if cached:
		query_res = get_quarry('30043','1')
		
		results = {f[2]:[f[0], ['en',f[1].replace('_',' ')]] for f in query_res}
		
		final2 = sort_list(results)
		saveToDB(final2,language,country,'en')
		return results
	else:
		query_res = run_queryEN(SQL_enwiki.format(country,language),toolforge.connect('enwiki_p','analytics'))
		result_json = [encode_all_items(f) for f in query_res]
		
		results = {f[2]:[f[0], ['en',f[1].replace('_',' ')]] for f in result_json}
		
		final2 = sort_list(results)
		saveToDB(final2,language,countryname,'en')
		
		return results
#

def ruwiki_query(countryname,language,country):
	pywikibot.output('ruwiki' + '\t'.join([countryname,language,country]))
	if cached:
		return {}
	else:
		query_res = run_query(SQL_ruwiki.format(country,language),toolforge.connect('ruwiki_p','analytics'))
		result_json = [encode_all_items(f) for f in query_res]
		frwikidata = {}
		
		for line in result_json:
			iws,fr,en,wd = line
			
			if en=='':
				frwikidata.update({wd:[iws,['ru',fr.replace('_',' ')]]})
			else:
				frwikidata.update({wd:[iws,['en',en]]})
		
		final2 = sort_list(frwikidata)
		saveToDB(final2,language,countryname,'ru')
		return frwikidata
#
sql_update = 'UPDATE `lists` SET jsondata=%s, last_upd=%s where wiki=%s and name=%s and list_type=%s and source=%s'

def saveToDB(jsonData,wiki,countryname,source):
	curr_time = utc_to_local(datetime.utcnow())
	currTime = "{0:%Y%m%d%H%M%S}".format(curr_time)
	
	string = sql_update % (str(json.dumps(jsonData)),currTime,wiki,countryname,"list",source)
	pywikibot.output(string)
	
#
def frwiki_query(countryname,language,country):
	pywikibot.output('frwiki' + '\t'.join([countryname,language,country]))
	if cached:
		query_res = get_quarry('30043','0')
		frwikidata = {}
		
		for line in query_res:
			iws,fr,en,wd = line
			
			if en=='':
				frwikidata.update({wd:[iws,['fr',fr.replace('_',' ')]]})
			else:
				frwikidata.update({wd:[iws,['en',en]]})
		
		final2 = sort_list(frwikidata)
		saveToDB(final2,language,country,'fr')
		return frwikidata
	else:
		query_res = run_query(SQL_frwiki.format(language,country),toolforge.connect('frwiki_p','analytics'))
		result_json = [encode_all_items(f) for f in query_res]
		frwikidata = {}
		
		for line in result_json:
			iws,fr,en,wd = line
			
			if en=='':
				frwikidata.update({wd:[iws,['fr',fr.replace('_',' ')]]})
			else:
				frwikidata.update({wd:[iws,['en',en]]})
		
		final2 = sort_list(frwikidata)
		saveToDB(final2,language,countryname,'fr')
		return frwikidata
#

def sort_list(thelist):
	final = []
	
	for one in thelist:
		thisdata = thelist[one]
		final.append([one,thisdata[0],thisdata[1]])
	
	final2 = sorted(final, key=lambda x: -int(x[1]))
	
	return final2

def main():
	languages = ['lv','et']
	countries = {'lv':{'en':'Latvia','fr':'Lettonie','ru':'Латвия'},'et':{'en':'Estonia','fr':'Estonie','ru':'Эстония'}}
	
	for country in countries:#kuras valsts saraksts tiek veidots
		if country=='et': continue#Latvija ir novembrī, to vēlāk
		
		countryname = 'Latvia'
		
		countrydata = countries[country]
		
		for wiki in languages:#kurai wiki šis saraksts domāts
			countryres = {}
			countryres.update(frwiki_query(countryname,wiki,countrydata['fr']))
			countryres.update(enwiki_query(countryname,wiki,countrydata['en']))
			countryres.update(ruwiki_query(countryname,wiki,countrydata['ru']))
			
			final2 = sort_list(countryres)
			saveToDB(final2,wiki,countryname,'all')
	
	#connLabs.close()
	conn.close()
	pywikibot.output('done')
	
#

#
main()