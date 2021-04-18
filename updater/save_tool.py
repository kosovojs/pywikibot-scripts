import toolforge
from datetime import datetime

data = eval(open('data/lv-data.txt','r',encoding='utf-8').read())

conn = toolforge.connect_tools('s53143__missing_p')
cursor = conn.cursor()

""" cursor.execute("TRUNCATE TABLE articles")
conn.commit()

sql = "INSERT INTO articles (wd, orig, lang, descr, wiki, iws) VALUES (%s, %s, %s, %s, %s, %s)"

for one in data:
	wd, orig, lang, descr, newwiki, iws = one
	cursor.execute(sql, (wd, orig, lang, descr, newwiki, iws))
#
conn.commit() """

dateforq12 = "{0:%Y-%m-%d}".format(datetime.utcnow())
sql2 = 'UPDATE meta set value= %s where data="upd" and wiki="lvwiki"'
cursor.execute(sql2, (dateforq12))
conn.commit()

conn.close()