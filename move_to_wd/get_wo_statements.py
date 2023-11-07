import re, os, sys, toolforge, logging

logging.basicConfig(filename='get_wo_statements.log', filemode='a+', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

conn = toolforge.connect('wikidatawiki_p','analytics')

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))

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
#

SQL_PAGE_ID = """select page_title, page_id
from page
WHERE page_namespace=0 AND page_is_redirect=0 AND page_title IN ({})"""

check_sql = """SELECT pp_page
FROM page_props
where pp_propname='wb-claims' AND pp_sortkey=0 AND pp_page in ({});"""

def get_items_wo_statements(items_to_check):
	items_to_check = list(items_to_check)
	cursor = conn.cursor()
	placeholders = ', '.join(['%s' for f in items_to_check])
	cursor.execute(check_sql.format(placeholders), items_to_check)
	#print(check_sql.format(placeholders))
	rows = cursor.fetchall()

	return [encode_if_necessary(f[0]) for f in rows]

def get_page_id(items_to_check):
	cursor = conn.cursor()
	placeholders = ', '.join(['%s' for f in items_to_check])
	cursor.execute(SQL_PAGE_ID.format(placeholders), ["Q{}".format(f) for f in items_to_check])
	#print(check_sql.format(placeholders))
	rows = cursor.fetchall()

	return {encode_if_necessary(f[1]):encode_if_necessary(f[0]) for f in rows}


SQLMAIN = """SELECT ips_item_id
FROM wb_items_per_site
where ips_site_id='lvwiki'"""

query_res = run_query(SQLMAIN,conn)

data = [encode_if_necessary(f[0]) for f in query_res]

def add_to_file(items):
	with open('data_las______.txt', 'a+', encoding='utf-8') as file_w:
		file_w.write(str(items)+"\n")

logging.info("Found {} items".format(len(data)))

cnt = 0

for chunk in chunker(data, 250):
	cnt += 1
	if cnt % 10 == 0:
		logging.info("\tcnt: {}".format(cnt))

	id_title_map = get_page_id(chunk)

	id_set = set(id_title_map)
	no_statements = set(get_items_wo_statements(id_set))

	#no_data.extend(diffr)
	if len(no_statements)>0:
		page_titles = [id_title_map.get(f, "FFF__{}".format(f)) for f in no_statements]
		add_to_file(page_titles)
		logging.info("Saved {} items".format(len(no_statements)))
logging.info("Finished")
#
