import pywikibot, re, os, requests, json
from datetime import date, datetime, timedelta
#from customFuncs import basic_petscan

site = pywikibot.Site("lv", "wikipedia")
site.login()
site.get_tokens('edit')

def do_api_req(wikipedia,title,cont=''):
	params = {
		"action": "query",
		"format": "json",
		"prop": "revisions",
		"titles": title,
		"rvprop": "timestamp|comment|user|ids|content",
		"rvlimit": "max",
		"rvdir": "older"
	}
	wikipedia = wikipedia.replace('wiki','').replace('_','-')

	if cont!='':
		params.update({"rvcontinue":cont})

	r = requests.get('https://{}.wikipedia.org/w/api.php?'.format(wikipedia),params = params)
	r.encoding = 'utf-8'
	json_data = eval(r.text)

	#print(json_data)
	#pywikibot.output(json_data["continue"])

	return json_data
#
def put_notif(title,user_orig,start_date,last_edit_obj):
	pagetosave = pywikibot.Page(site,'Diskusija:'+title)
	pgtext = pagetosave.text

	if 'pievienojis šai lapai veidni' in pgtext: return 0

	cur_date = datetime.now()
	text = """{{{{ping|{}}}}} Tu esi pievienojis šai lapai veidni {{{{tl|inuse}}}} un pēdējā laikā neesi aktīvi darbojies: veidne ielikta pirms {} dienām un pēdējo labojumu esi veicis pirms {} dienām. Lūdzu izvērtē, vai Tu tiešām '''aktīvi''' strādā pie šīs lapas un tai ir tiešām nepieciešama {{{{tl|inuse}}}} veidne. Ja ne, tad lūgums lapu uzlabot un noņemt veidni. Paldies! --~~~~""".format(
		user_orig, (cur_date-start_date).days, (cur_date-last_edit_obj).days
	)#user_orig,

	r = pywikibot.data.api.Request(site=site, action='edit', format='json', bot=0, title='Diskusija:'+title, section='new', sectiontitle='Inuse veidne', text=text,token=site.tokens['edit'], summary='inuse veidnes lietojums').submit()
#
inuseregex = '{{\s*(template:|veidne:)?\s*(inuse|under[_ ]construction|labošanā|in[_ ]use|inuseuntil|lietošanā|rediģēšanā)\s*}}'#|ilgstošā[_ ]labošanā|ilgstošā[_ ]lietošanā|ilgstošā[_ ]rediģēšanā|inuse2|long[_ ]inuse|underconstruction

def parse_one_article(title,file):
	#file = eval(open("inuse.json", "r", encoding='utf-8').read())

	file = file['query']['pages']
	theid = list(file.keys())[0]

	counter = 0

	firstRevWithTpl = None#labojums, kurā dalībnieks pieliek veidni
	lastRevWithoutTpl = None#pēdējais labojums bez veidnes


	for rev in file[theid]['revisions']:
		revtext = rev['*']
		hasinuse = re.search(inuseregex,revtext,re.I)
		#print(('yes' if hasinuse else 'NO'), rev['timestamp'])
		if not hasinuse:
			#lastRevWithoutTpl = rev
			break
		else:
			firstRevWithTpl = rev
	#
	#print([lastRevWithoutTpl, firstRevWithTpl])


	date_from = firstRevWithTpl['timestamp']
	user_orig = firstRevWithTpl['user']
	#print(date_from)
	#print(user_orig)
	#
	last_edit = ''
	for rev in file[theid]['revisions']:
		if rev['user']==user_orig:
			last_edit = rev['timestamp']
			break
	#
	#print(last_edit)

	date_format = "%m/%d/%Y"
	cur_date = datetime.now()
	start_date = datetime.strptime(date_from,'%Y-%m-%dT%H:%M:%SZ')
	last_edit_obj = datetime.strptime(last_edit,'%Y-%m-%dT%H:%M:%SZ')

	print({'user_last':user_orig,'date_first_edit':date_from,'date_last_edit_by_user':last_edit,'diff':(cur_date-start_date).days, 'diff2': (cur_date-last_edit_obj).days})

	if (cur_date-start_date).days>10 and (cur_date-last_edit_obj).days>7:
		print('larger, will put notif')
		put_notif(title,user_orig,start_date,last_edit_obj)
#
def getAllPages():
	params = {
		"action": "query",
		"format": "json",
		"list": "categorymembers",
		"utf8": 1,
		"formatversion": "2",
		"cmtitle": "Kategorija:Lapas, ko šobrīd pārstrādā",
		"cmprop": "title",
		"cmlimit": "max"
	}
	wikipedia = 'lv'

	r = requests.get('https://{}.wikipedia.org/w/api.php?'.format(wikipedia),params = params)
	r.encoding = 'utf-8'
	json_data = json.loads(r.text)['query']['categorymembers']
	json_data = [f['title'].replace(' ','_') for f in json_data]
	return json_data

def main():
	#Latvijas putnu sugu saraksts - pagaidām ignorēt
	#listarticles = basic_petscan('4534095')
	#listarticles = [f['title'] for f in listarticles]
	listarticles = getAllPages()

	for onearticle in listarticles:
		#if onearticle=='Rokenrola_slavas_zāle': continue
		apivesture = do_api_req('lvwiki',onearticle)
		#rchanges = apivesture['query']["pages"]
		#theid = list(rchanges.keys())
		print('*'*60)
		pywikibot.output(onearticle)
		parse_one_article(onearticle,apivesture)
#
main()
