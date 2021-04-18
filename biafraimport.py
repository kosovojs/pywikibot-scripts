import pywikibot, re, os, requests
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone
#from customFuncs import basic_petscan
from natsort import natsorted
import pymysql

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

conn = toolforge.connect_tools('s53143__npp_p')
conn1 = toolforge.connect('lvwiki_p','analytics')

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

def local_to_utc(utc):
	return lva_timezone.localize(utc).astimezone(utc_timezone)
#
def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection):
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




max_time = encode_if_necessary(run_query("select max(date) from main",conn)[0][0])
#dtobject = datetime.strptime(max_time, '%Y%m%d%H%M%S')
date_string = "{0:%Y%m%d%H%M%S}".format(local_to_utc(max_time))

print('NPP import: maximal timestamp curr db: '+str(max_time))
print('NPP import: maximal timestamp curr db -> utc: '+str(date_string))
#print('maxtime conv: '+str(local_to_utc(max_time)))
#print('dtobject: '+dtobject)
#print('date_string: '+str(date_string))

#os.chdir(r'projects/lv')

#file = eval(open("quarry-27666-untitled-run268322.json", "r", encoding='utf-8').read())['rows']


file = run_query('select rev_user_text, rev_timestamp, orig.page_title from revision join page orig on orig.page_id=rev_page and orig.page_is_redirect=0 and orig.page_namespace=0 where rev_timestamp>"{}" and rev_parent_id=0'.format(date_string),conn1)



file = natsorted(file, key=lambda x: encode_if_necessary(x[1]))
#http://pymysql.readthedocs.io/en/latest/user/examples.html

article_count = run_query('SELECT count(*) FROM main WHERE (comment is NULL and reviewed is NULL)',conn)
article_count = encode_if_necessary(article_count[0][0])


def run_upd(query):
	#query = query.encode('utf-8')
	#print(query)
	try:
		#https://askubuntu.com/questions/1026770/can-not-insert-data-mysql-using-python-with-pymysql
		cursor = conn.cursor()
		cursor.execute(query)
		conn2.commit()
	except KeyboardInterrupt:
		sys.exit()
#
cursor = conn.cursor()

localtime2 = utc_to_local(datetime.utcnow())
dateforq12 = "{0:%Y%m%d%H%M%S}".format(localtime2)

sql2 = 'INSERT INTO `stats` (`timest`, `articles`) VALUES (%s, %s)'
cursor.execute(sql2, (dateforq12,article_count))

print('NPP import: found: '+str(len(file)))

for row in file:
	row = [encode_if_necessary(f) for f in row]
	user,date,article = row
	
	if article in ('Krasnoslobodska','Krasnoslobodska_(Mordvija)'): continue
	
	parsed_date = datetime.strptime(date,'%Y%m%d%H%M%S')
	localtime = utc_to_local(parsed_date)
	dateforq1 = "{0:%Y%m%d%H%M%S}".format(localtime)
	#print(dateforq1)
	sql = 'INSERT INTO `main` (`title`, `date`, `user`) VALUES (%s, %s, %s)'
	
	#cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
	cursor.execute(sql, (article.replace('_',' '),dateforq1,user.replace('_',' ')))
#
#
conn.commit()
conn.close()