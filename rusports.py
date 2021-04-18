import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

conn = toolforge.connect('ruwiki_p','analytics')
#connLabs = toolforge.connect_tools('s53143__mis_lists_p')
#cursor1 = connLabs.cursor()

cats = [{"id":7641522,"len":216,"n":"page","namespace":14,"nstext":"Категория","title":"Пилоты_24_часов_Ле-Мана_по_алфавиту","touched":"20181022120650"},{"id":636192,"len":188,"n":"page","namespace":14,"nstext":"Категория","title":"Боксёры_по_алфавиту","touched":"20181208184543"},{"id":636668,"len":196,"n":"page","namespace":14,"nstext":"Категория","title":"Биатлонисты_по_алфавиту","touched":"20181207090121"},{"id":641610,"len":192,"n":"page","namespace":14,"nstext":"Категория","title":"Хоккеисты_по_алфавиту","touched":"20181208132614"},{"id":648652,"len":193,"n":"page","namespace":14,"nstext":"Категория","title":"Футболисты_по_алфавиту","touched":"20181208154504"},{"id":655030,"len":192,"n":"page","namespace":14,"nstext":"Категория","title":"Дзюдоисты_по_алфавиту","touched":"20181123061455"},{"id":789089,"len":136,"n":"page","namespace":14,"nstext":"Категория","title":"Спидвейные_гонщики_по_алфавиту","touched":"20181205165035"},{"id":1063323,"len":196,"n":"page","namespace":14,"nstext":"Категория","title":"Конькобежцы_по_алфавиту","touched":"20181028173859"},{"id":1563380,"len":125,"n":"page","namespace":14,"nstext":"Категория","title":"Снукеристы_по_алфавиту","touched":"20181118105206"},{"id":1718316,"len":198,"n":"page","namespace":14,"nstext":"Категория","title":"Сноубордисты_по_алфавиту","touched":"20181126211108"},{"id":1726764,"len":142,"n":"page","namespace":14,"nstext":"Категория","title":"Игроки_в_мини-футбол_по_алфавиту","touched":"20181208153702"},{"id":1759130,"len":159,"n":"page","namespace":14,"nstext":"Категория","title":"Велогонщики_по_алфавиту","touched":"20181208184808"},{"id":1770846,"len":125,"n":"page","namespace":14,"nstext":"Категория","title":"Теннисисты_по_алфавиту","touched":"20181118183945"},{"id":1820363,"len":199,"n":"page","namespace":14,"nstext":"Категория","title":"Шорт-трекисты_по_алфавиту","touched":"20180903103101"},{"id":1822620,"len":198,"n":"page","namespace":14,"nstext":"Категория","title":"Горнолыжники_по_алфавиту","touched":"20181208174901"},{"id":1843706,"len":198,"n":"page","namespace":14,"nstext":"Категория","title":"Скелетонисты_по_алфавиту","touched":"20181120171034"},{"id":1845090,"len":194,"n":"page","namespace":14,"nstext":"Категория","title":"Бобслеисты_по_алфавиту","touched":"20181203131346"},{"id":1855810,"len":192,"n":"page","namespace":14,"nstext":"Категория","title":"Саночники_по_алфавиту","touched":"20181205190903"},{"id":1892580,"len":188,"n":"page","namespace":14,"nstext":"Категория","title":"Лыжники_по_алфавиту","touched":"20181202193320"},{"id":1911610,"len":344,"n":"page","namespace":14,"nstext":"Категория","title":"Баскетболисты_по_алфавиту","touched":"20181207120352"},{"id":1972369,"len":192,"n":"page","namespace":14,"nstext":"Категория","title":"Фигуристы_по_алфавиту","touched":"20181208015528"},{"id":2145612,"len":142,"n":"page","namespace":14,"nstext":"Категория","title":"Бейсболисты_по_алфавиту","touched":"20181130102708"},{"id":2289970,"len":115,"n":"page","namespace":14,"nstext":"Категория","title":"Борцы_по_алфавиту","touched":"20181115125907"},{"id":2404493,"len":226,"n":"page","namespace":14,"nstext":"Категория","title":"Гандболисты_по_алфавиту","touched":"20181206211042"},{"id":3320851,"len":121,"n":"page","namespace":14,"nstext":"Категория","title":"Самбисты_по_алфавиту","touched":"20180610115418"},{"id":3420138,"len":113,"n":"page","namespace":14,"nstext":"Категория","title":"Игроки_го_по_алфавиту","touched":"20181004153752"},{"id":3519842,"len":107,"n":"page","namespace":14,"nstext":"Категория","title":"Курашисты_по_алфавиту","touched":"20180502160727"},{"id":3640339,"len":224,"n":"page","namespace":14,"nstext":"Категория","title":"Гребцы_на_байдарках_и_каноэ_по_алфавиту","touched":"20180903103102"},{"id":3642592,"len":239,"n":"page","namespace":14,"nstext":"Категория","title":"Парапланеристы_по_алфавиту","touched":"20180503122706"},{"id":4264700,"len":210,"n":"page","namespace":14,"nstext":"Категория","title":"Прыгуны_с_трамплина_по_алфавиту","touched":"20181201182902"},{"id":4391445,"len":121,"n":"page","namespace":14,"nstext":"Категория","title":"Регбисты_по_алфавиту","touched":"20181114233807"},{"id":4470121,"len":192,"n":"page","namespace":14,"nstext":"Категория","title":"Двоеборцы_по_алфавиту","touched":"20181129101626"},{"id":4475227,"len":146,"n":"page","namespace":14,"nstext":"Категория","title":"Раллисты_по_алфавиту","touched":"20180110075702"},{"id":4721655,"len":196,"n":"page","namespace":14,"nstext":"Категория","title":"Автогонщики_по_алфавиту","touched":"20181208183821"},{"id":4721658,"len":205,"n":"page","namespace":14,"nstext":"Категория","title":"Пилоты_Формулы-1_по_алфавиту","touched":"20181006152402"},{"id":4737563,"len":180,"n":"page","namespace":14,"nstext":"Категория","title":"Легкоатлеты_по_алфавиту","touched":"20181130104316"},{"id":4772887,"len":127,"n":"page","namespace":14,"nstext":"Категория","title":"Мотогонщики_по_алфавиту","touched":"20181129050853"},{"id":4803524,"len":114,"n":"page","namespace":14,"nstext":"Категория","title":"Сёгисты_по_алфавиту","touched":"20181004153913"},{"id":4901188,"len":198,"n":"page","namespace":14,"nstext":"Категория","title":"Фристайлисты_по_алфавиту","touched":"20181112205606"},{"id":4912886,"len":127,"n":"page","namespace":14,"nstext":"Категория","title":"Кёрлингисты_по_алфавиту","touched":"20181208061923"},{"id":4936313,"len":209,"n":"page","namespace":14,"nstext":"Категория","title":"Спортсмены-ведущие_по_алфавиту","touched":"20180903103102"},{"id":5642965,"len":204,"n":"page","namespace":14,"nstext":"Категория","title":"Киберспортсмены_по_алфавиту","touched":"20181120232831"},{"id":5853561,"len":160,"n":"page","namespace":14,"nstext":"Категория","title":"Ориентировщики_по_алфавиту","touched":"20181130134318"},{"id":5870042,"len":121,"n":"page","namespace":14,"nstext":"Категория","title":"Яхтсмены_по_алфавиту","touched":"20181104211941"},{"id":6548909,"len":123,"n":"page","namespace":14,"nstext":"Категория","title":"Гольфисты_по_алфавиту","touched":"20181005070616"},{"id":6610082,"len":225,"n":"page","namespace":14,"nstext":"Категория","title":"Волейболисты_по_алфавиту","touched":"20181207020651"},{"id":6717263,"len":134,"n":"page","namespace":14,"nstext":"Категория","title":"Культуристы_по_алфавиту","touched":"20180903103101"},{"id":6763126,"len":184,"n":"page","namespace":14,"nstext":"Категория","title":"Шахматисты_по_алфавиту","touched":"20181208120158"},{"id":6843826,"len":389,"n":"page","namespace":14,"nstext":"Категория","title":"Ралли-кроссмены_по_алфавиту","touched":"20181119210755"},{"id":7180955,"len":115,"n":"page","namespace":14,"nstext":"Категория","title":"Бадминтонисты_по_алфавиту","touched":"20180613195845"},{"id":7276427,"len":228,"n":"page","namespace":14,"nstext":"Категория","title":"Велогонщицы_по_алфавиту","touched":"20181118094315"},{"id":7339878,"len":199,"n":"page","namespace":14,"nstext":"Категория","title":"Бойцы_смешанных_единоборств_по_алфавиту","touched":"20181205130125"}]
cats = [f['title'] for f in cats]

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
#, (select m2.ll_title from langlinks m2 where m2.ll_from=l.ll_from and m2.ll_lang="en")  as en
SQL_main = """select p.page_title, count(l.ll_lang) as langs, ""
from langlinks l
join page p on p.page_id=l.ll_from
and p.page_namespace=0 and not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
	and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
               										and cla.cl_to="{}"
               )
group by l.ll_from
order by count(l.ll_lang) desc
limit 1000;"""

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

#infoboxlist = infoboxlist[::-1]

sql_insert = 'INSERT INTO `entries` (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'
#sql_update = 'UPDATE `entries` SET jsondata=%s, last_upd=%s, name=%s where id=%s'

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def main():
	for infobox in cats:
		sys.stdout.flush()
		begin = time.time()
		#result_json = []
		query_res = run_query(SQL_main.format(infobox))
		
		end = time.time()
		timelen = end-begin
		if timelen>30:
			pywikibot.output('{}'.format(timelen))
		
		result_json = [encode_all_items(f) for f in query_res]
		curr_time = utc_to_local(datetime.utcnow())
		dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
		#print(dateforq1)
		
		#put_db(infobox,result_json,dateforq1)
		#cursor1.execute(sql_insert, (infobox.replace('Infobox_','').replace('_',' '), 'eninfobox',str(json.dumps(result_json)),dateforq1))
		
		#pywikibot.output(SQL_main.format(newtitle))
		pywikibot.output(result_json[:3])
		
		connLabs = toolforge.connect_tools('s53143__mis_lists_p')
		cursor1 = connLabs.cursor()
		cursor1.execute(sql_insert, (infobox.replace('_по_алфавиту','').replace('_',' '),'rusports',str(json.dumps(result_json, ensure_ascii=False)),dateforq1))
		
		connLabs.commit()
		connLabs.close()
	conn.close()
	pywikibot.output('done')
		
#
main()