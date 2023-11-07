import re, os, sys, toolforge, logging
from gather_info import get_labels_from_wikidata

logging.basicConfig(filename='get_wo_labels_.log', filemode='a+', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

check_sql = """SELECT
  wbit_item_id as id
FROM wbt_item_terms
JOIN wbt_term_in_lang ON wbit_term_in_lang_id = wbtl_id
JOIN wbt_type ON wbtl_type_id = wby_id
JOIN wbt_text_in_lang ON wbtl_text_in_lang_id = wbxl_id
WHERE wbit_item_id in ({}) and wby_name='label' and wbxl_language='lv';"""

def get_items_with_labels(items_to_check):
	cursor = conn.cursor()
	placeholders = ', '.join(['%s' for f in items_to_check])
	cursor.execute(check_sql.format(placeholders), items_to_check)
	#print(check_sql.format(placeholders))
	rows = cursor.fetchall()

	return [encode_if_necessary(f[0]) for f in rows]


SQLMAIN = """SELECT ips_item_id
FROM wb_items_per_site
where ips_site_id='lvwiki'"""

query_res = run_query(SQLMAIN,conn)

data = [encode_if_necessary(f[0]) for f in query_res]

def add_to_file(items):
	with open('data_last__.txt', 'a+', encoding='utf-8') as file_w:
		file_w.write(str(items)+"\n")

logging.info("Found {} items".format(len(data)))

cnt = 0
all_missing_ids = []

for chunk in chunker(data, 1000):
	cnt += 1
	if cnt % 10 == 0:
		logging.info("\tcnt: {}".format(cnt))
	has_label = set(get_items_with_labels(chunk))
	diffr = list(set(chunk) - has_label)
	#no_data.extend(diffr)
	if len(diffr)>0:
		add_to_file(diffr)
		logging.info("Saved {} items".format(len(diffr)))
		all_missing_ids.extend(diffr)

logging.info("Finished gathering data")
logging.info("starting second phase")

get_labels_from_wikidata(all_missing_ids)
logging.info("finished second phase")
#
