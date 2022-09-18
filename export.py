import re, os, sys
import pywikibot
import html, toolforge
from pywikibot import xmlreader
from bz2 import BZ2File
import mwparserfromhell

conn = toolforge.connect_tools('s53143__meta_p')
conn_wiki = toolforge.connect('lvwiki_p')
paths = '/public/dumps/public/lvwiki/latest/lvwiki-latest-pages-articles.xml.bz2'

num = 0
numprint = 10_000

def pagename(bg):
	bg = re.sub('\s*(\([^\(]+)$','',bg)

	return bg

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(sql):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn_wiki.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows


def get_redirects():
	sql_query = 'Select page_title from page where page_namespace=0'
	lvwiki = run_query(sql_query)

	return [encode_if_necessary(b[0]).replace('_',' ') for b in lvwiki]

def capitalize(inp):
	if len(inp)<1:
		return inp

	return inp[0].upper() + inp[1:]

def getCurrentTime():
	from time import gmtime, strftime
	currTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())#'2009-01-05 22:14:39'
	return currTime

def get_text_till_heading(input_text):
	heading = re.search(r'^={1,}[^=]+={1,}\s*$', input_text, re.MULTILINE)

	if not heading:
		return input_text

	return input_text[:heading.start()]


CURRENT_REDIRECTS = get_redirects()

def get_suggestion_title(input_text):
	repl = re.sub("^'{3,5}", '', input_text)
	return re.sub("'{3,5}$", '', repl)

def insert_many_at_once(table, cols, rows):
	with conn.cursor() as cursor:
		valueTupleTpl = "({})".format(', '.join(['%s'] * len(cols)))

		insertTpl = 'INSERT INTO {} ({}) values {}'.format(
			table,
			','.join(cols),
			','.join(valueTupleTpl for _ in rows)
		)

		values = [_ for r in rows for _ in r]

		#print(insertTpl, values, flush=True)

		cursor.execute(insertTpl, values)
		conn.commit()

def clean_text(input_text):
	input_text = re.sub('<!--.*?-->', '',input_text)#remove comments
	input_text = re.sub('<ref([^>]+)\/>', '',input_text)#remove self-closing reference tags
	input_text = re.sub('<ref((?!<\/ref>).)*<\/ref>', '',input_text)#remove references
	input_text = re.sub('<ref([^>]+)>', '',input_text)#remove reference tags

	return input_text

def handle_article(article_title, text):
	cleaned = clean_text(text)
	pagenamed_title = pagename(article_title)

	analyzable_text = get_text_till_heading(cleaned)
	wikicode = mwparserfromhell.parse(analyzable_text)
	#print(dir(wikicode))

	nodes = wikicode.nodes

	bolded_texts = []

	for node in nodes:
		#print(mwparserfromhell.parse(node).filter_text())
		if (node.startswith("'''''") and node.endswith("'''''")) \
			or (node.startswith("'''") and node.endswith("'''")):
			bolded_texts.append(capitalize(get_suggestion_title(str(node))))
	#print()
	#print(article_title)
	bolded_texts = list(set(bolded_texts))

	final_list = []

	for res in bolded_texts:
		if len(res)<3: continue
		if res == pagenamed_title or res == article_title: continue
		if res in CURRENT_REDIRECTS: continue
		final_list.append(res)

	return final_list

to_insert = []

with BZ2File(paths) as xml_file:
	blah = False
	for page in xmlreader.XmlDump(paths).parse():
		if page.ns != "0" or page.isredirect: continue

		pagetext = html.unescape(page.text)
		pagetitle = page.title

		#if pagetitle != '6. Saeimas vēlēšanas': continue


		num += 1
		if num % numprint == 0:
			print(num)
			#print(getCurrentTime())
			sys.stdout.flush()
			#exit()


		suggested_redirects = handle_article(pagetitle, pagetext)

		tmp_data = []

		for one in suggested_redirects:
			tmp_data.append([pagetitle, one, None, getCurrentTime(), None])

		to_insert.extend(tmp_data)

		if len(to_insert)>1000:
			insert_many_at_once('redirector', ['article_title', 'suggested_title', 'edited_title', 'added_at', 'completed_at'], to_insert)
			to_insert = []

if len(to_insert)>0:
	insert_many_at_once('redirector', ['article_title', 'suggested_title', 'edited_title', 'added_at', 'completed_at'], to_insert)
	to_insert = []
