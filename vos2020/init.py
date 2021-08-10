from handle_missing import MissingArticlesHandler
import pymysql, json
import toolforge
import sys

mode = sys.argv[1] if len(sys.argv)>1 else 'allwikis'


inst = MissingArticlesHandler('lvwiki')


if mode == 'allwikis':
	data_to_save = inst.handle_all_wikis('Q66827758', 2)

if mode == 'en_sub':
	data_to_save = inst.subcats('enwiki', 'Category:Competitors at the 2020 Summer Olympics')

sql_q = """INSERT INTO entries (name, group_name, jsondata) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE jsondata =  %s"""

conn_meta = toolforge.connect('mis_lists_p')
cursor = conn_meta.cursor()

json_data_to_save = json.dumps(data_to_save)
cursor.execute(sql_q, (mode, 'vos2020', json_data_to_save, json_data_to_save))
conn_meta.commit()
