import pywikibot, re, os, requests
from datetime import date, datetime, timedelta
from customFuncs import basic_petscan

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
inuseregex = '{{\s*(template:|veidne:)?\s*(inuse|under[_ ]construction|labošanā|in[_ ]use|inuseuntil|lietošanā|rediģēšanā|ilgstošā[_ ]labošanā|ilgstošā[_ ]lietošanā|ilgstošā[_ ]rediģēšanā|inuse2|long[_ ]inuse|underconstruction)\s*}}'

def parse_one_article(title,file):
	#file = eval(open("inuse.json", "r", encoding='utf-8').read())

	file = file['query']['pages']
	theid = list(file.keys())[0]

	counter = 0
	for rev in file[theid]['revisions']:
		revtext = rev['*']
		hasinuse = re.search(inuseregex,revtext,re.I)
		counter += 1
		if hasinuse:
			continue
		else:
			break
	#
	print(counter)

	if counter == len(file[theid]['revisions']):
		neededrev = file[theid]['revisions'][-1]
	else:
		neededrev = file[theid]['revisions'][counter-2]
	#
	date_from = neededrev['timestamp']
	user_orig = neededrev['user']
	print(date_from)
	print(user_orig)
	#
	last_edit = ''
	for rev in file[theid]['revisions']:
		if rev['user']==user_orig:
			last_edit = rev['timestamp']
			break
	#
	print(last_edit)

	date_format = "%m/%d/%Y"
	cur_date = datetime.now()
	start_date = datetime.strptime(date_from,'%Y-%m-%dT%H:%M:%SZ')
	last_edit_obj = datetime.strptime(last_edit,'%Y-%m-%dT%H:%M:%SZ')

	if (cur_date-start_date).days>10 and (cur_date-last_edit_obj).days>7:
		print('larger, will put notif')
		put_notif(title,user_orig,start_date,last_edit_obj)
#
def main():
	#Latvijas putnu sugu saraksts - pagaidām ignorēt
	listarticles = basic_petscan('4534095')
	#listarticles = {"n":"result","a":{"querytime_sec":0.011363,"query":"https://petscan.wmflabs.org/?active_tab=tab_pageprops&after=&before=&categories=Lapas%2C%20ko%20%C5%A1obr%C4%ABd%20p%C4%81rstr%C4%81d%C4%81&cb_labels_any_l=1&cb_labels_no_l=1&cb_labels_yes_l=1&combination=subset&common_wiki=auto&depth=0&doit=Do%20it%21&edits%5Banons%5D=both&edits%5Bbots%5D=both&edits%5Bflagged%5D=both&format=json&interface_language=en&labels_any=&labels_no=&labels_yes=&langs_labels_any=&langs_labels_no=&langs_labels_yes=&language=lv&larger=&links_to_all=&links_to_any=&links_to_no=&manual_list=&manual_list_wiki=&max_age=&max_sitelink_count=&maxlinks=&min_redlink_count=1&min_sitelink_count=&minlinks=&negcats=&ns%5B0%5D=1&ores_prediction=any&ores_prob_from=&ores_prob_to=&ores_type=any&outlinks_any=&outlinks_no=&outlinks_yes=&output_compatability=catscan&page_image=any&pagepile=&project=wikipedia&regexp_filter=&show_redirects=both&sitelinks_any=&sitelinks_no=&sitelinks_yes=&smaller=&sortby=none&sortorder=ascending&source_combination=&sparql=&subpage_filter=either&templates_any=&templates_no=&templates_yes=&wikidata_item=no&wikidata_label_language=&wikidata_prop_item_use=&wikidata_source_sites=&wpiu=any"},"*":[{"n":"combination","a":{"type":"subset","*":[{"id":103594,"len":64193,"n":"page","namespace":0,"nstext":"","title":"Latvijas_putnu_sugu_saraksts","touched":"20180514174705"},{"id":215304,"len":1404,"n":"page","namespace":0,"nstext":"","title":"Glodene","touched":"20180514191653"},{"id":380614,"len":8106,"n":"page","namespace":0,"nstext":"","title":"Luka_Pačoli","touched":"20180429095833"},{"id":382459,"len":16308,"n":"page","namespace":0,"nstext":"","title":"Aleksandrs_Godunovs","touched":"20180504082815"},{"id":385257,"len":14413,"n":"page","namespace":0,"nstext":"","title":"Pasaules_šaha_čempionāts_sievietēm","touched":"20180518190603"},{"id":396158,"len":3539,"n":"page","namespace":0,"nstext":"","title":"Sārtgalvītis","touched":"20180518094952"},{"id":396160,"len":1651,"n":"page","namespace":0,"nstext":"","title":"Zeltgalvītis","touched":"20180514175205"},{"id":396163,"len":1492,"n":"page","namespace":0,"nstext":"","title":"Glodeņu_dzimta","touched":"20180514190516"},{"id":396168,"len":1196,"n":"page","namespace":0,"nstext":"","title":"Glodenes","touched":"20180514191517"},{"id":396502,"len":1699,"n":"page","namespace":0,"nstext":"","title":"Līkņu_modelēšana","touched":"20180519191728"}]}}]}
	#listarticles = listarticles['*'][0]['a']['*']
	listarticles = [f['title'] for f in listarticles]
	
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