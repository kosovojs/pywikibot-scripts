import toolforge, pywikibot
conn = toolforge.connect('lvwiki_p')  # You can also use "enwiki_p"
# conn is a pymysql.connection object.
with conn.cursor() as cur:
    query = "select * from revision where rev_timestamp>20180101010000 limit 10;"
    cur.execute(query)  # Or something....
    pywikibot.output(cur.fetchall())