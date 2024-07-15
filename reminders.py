import pywikibot, sys
import toolforge
import pytz, datetime

site = pywikibot.Site("lv", "wikipedia")
conn = toolforge.toolsdb('s53143__meta_p')


my_date1 = datetime.datetime.now(pytz.timezone('Europe/Riga'))
dateforq1 = "{:%Y-%m-%d %H:%M:%S}".format(my_date1)

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
def run_upd(query):
	#query = query.encode('utf-8')
	#print(query)
	try:
		#https://askubuntu.com/questions/1026770/can-not-insert-data-mysql-using-python-with-pymysql
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
	except KeyboardInterrupt:
		sys.exit()

#
data = run_query('select id, page, comment, page_notif, ping_user from reminders__main where archive is NULL and completed is NULL and (notif_time is NULL or "{}">notif_time)'.format(dateforq1))

def put_data(id,page,user,comm,page_comm=''):
	pagesave = pywikibot.Page(site,page)

	#try:
	if pagesave.exists():
		text = pagesave.get()+'\n\n'
	else:
		text = ''

	if comm!='':
		comm = 'Atstātais komentārs:\n:{}\n'.format(comm)
	if page_comm!='':
		page_comm = ' Lapa: {}\n'.format(page_comm)
	else:
		comm = ' '+comm

	text += '== Atgādinājums ==\nSveiks, {{{{u|{}}}}}! Tu (vai kāds cits) pieprasīja [http://tools.wmflabs.org/edgars/reminders/ atgādinājumu].{}{}--~~~~'.format(user,page_comm,comm)
	#pywikibot.output(text)
	pagesave.text = text
	pagesave.save(summary='Atgādinājums', botflag=True, minor=False)
	my_date = datetime.datetime.now(pytz.timezone('Europe/Riga'))
	dateforq = "{:%Y-%m-%d %H:%M:%S}".format(my_date)
	#print(dateforq)

	id = int(id)
	run_upd('UPDATE reminders__main SET completed="{}" WHERE id={}'.format(dateforq,id))
	#except:
	#	print('unsucc')
#

for row in data:
	row = [encode_if_necessary(f) for f in row]
	#id, page, comment, page_notif, ping_user
	pywikibot.output(row)
	page = row[1]
	pageid = row[0]
	comment = row[2]
	page_notif = row[3]
	ping_user = row[4]

	#if page=='Edgars2007':
	#	page='Experts'

	#if ping_user=='Edgars2007':
	#	ping_user='Experts'

	if page=='' and page_notif in ('thepage','talk'): continue

	if page_notif=='notifpage':
		put_data(pageid,'Vikipēdija:Atgādinājumi',ping_user,comment,page)

	elif page_notif=='usertalk':
		sdfsdfsdfsfs = pywikibot.Page(site,'Dalībnieka diskusija:'+ping_user)
		#if sdfsdfsdfsfs.isTalkPage():
		put_data(pageid,'Dalībnieka diskusija:'+ping_user,ping_user,comment)
		#else:
		#	page = sdfsdfsdfsfs.toggleTalkPage().title()
		#	put_data(pageid,page,ping_user,comment)

	elif page_notif=='thepage':
		sdfsdfsdfsfs = pywikibot.Page(site,page)
		#print('-'+str(sdfsdfsdfsfs.namespace())+'-')
		if str(sdfsdfsdfsfs.namespace())==':':
			page = 'Diskusija:'+page
			put_data(pageid,page,ping_user,comment)
		else:
			put_data(pageid,page,ping_user,comment)

	elif page_notif=='talk':
		sdfsdfsdfsfs = pywikibot.Page(site,page)
		page = sdfsdfsdfsfs.toggleTalkPage().title()
		put_data(pageid,page,ping_user,comment)
