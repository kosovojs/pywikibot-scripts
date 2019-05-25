import pywikibot, re, os, requests
from datetime import date, datetime, timedelta
from customFuncs import basic_petscan
from pywikibot import textlib

site = pywikibot.Site("lv", "wikipedia")
site.login()
site.get_tokens('edit')

#os.chdir(r'projects/lv')

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
inuseregex = '{{\s*(template:|veidne:)?\s*(dzēst|delete)( attēlu)?'

def get_infobox_params(pagetext):
	tplnames = ['dzēst','delete','dzēst attēlu']
	
	infobox = {}
	
	for template, fielddict in textlib.extract_templates_and_params(pagetext, remove_disabled_parts=False, strip=True):
		tplname = template.lower().strip().replace('_',' ')
		if tplname in tplnames:
			infobox = {f[0]:f[1] for f in fielddict.items()}
			#fileobj.write(str(thisrow))
			#if len(parsed) % 25 == 0:
			#	print(len(parsed))
			#pywikibot.output(infobox)
			break
	
	
	return infobox
#
def parse_one_article(title,file):
	#file = eval(open("inuse.json", "r", encoding='utf-8').read())

	file = file['query']['pages']
	theid = list(file.keys())[0]

	counter = 0
	if 'revisions' not in file[theid]: return
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

	#if counter == len(file[theid]['revisions']):
	#	neededrev = file[theid]['revisions'][-1]
	#else:
	neededrev = file[theid]['revisions'][counter-2]
	#
	date_from = neededrev['timestamp']
	user_orig = neededrev['user']
	commentars = neededrev['comment']
	
	pagetosave = pywikibot.Page(site,title)
	pgtext = pagetosave.text
	
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
	
	return [start_date,user_orig,commentars,get_infobox_params(pgtext)]
#.strftime('%Y-%m-%dT%H:%M:%SZ')
def makeTable(data):
	
	beigas = []
	apid = []
	
	data.sort(key=lambda x: x[0][0])
	#
	for one in data:
		reald,apis = one
		thisrow = "| {{{{page-multi|page={}|t|h|d}}}} || {} || {} || {{{{U|{}}}}} || <nowiki>{}</nowiki> || {}\n|-".format(reald[4].replace('_',' '),reald[0].strftime('%Y-%m-%d %H:%M:%S'),(datetime.now() - reald[0]).days,reald[1],reald[2],reald[3]['1'] if '1' in reald[3] else '')
		beigas.append(thisrow)
		apid.append(apis)
	#
	tosave = '<div style="float:right;">{{Tnavbar|Dzēšanai izvirzītās lapas|mini=1}}</div>\nAtjaunināts: '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'{{clear}}\n{| class="sortable wikitable"\n|-\n! Lapa || Izvirzīšanas datums || Dienu skaits || Izvirzītājs || Kopsavilkuma komentārs || Pamatojums veidnē\n|-\n'+'\n'.join(beigas)+'\n|}<noinclude>\n[[Kategorija:Vikipēdijas veidnes]]</noinclude>'
	
	saglapa = pywikibot.Page(site,'Veidne:Dzēšanai izvirzītās lapas')
	saglapa.text = tosave
	saglapa.save(summary='upd', botflag=False, minor=False)
	
	#with open("dfsdfsdfsdf.txt", "w", encoding='utf-8') as fileS:
	#	fileS.write(tosave+'\n\n\n\n'+str(apid))
	
	
def main():
	listarticles = basic_petscan('6538079')
	listarticles = [f for f in listarticles]
	
	sdf = []
	
	for onearticle in listarticles:
		if onearticle in ('Kategorija:NowCommons','Kategorija:Dzēšanai_izvirzītie_attēli','Kategorija:Db-commons','Kategorija:Dzēšanai_izvirzītās_lapas','Veidne:Dzēšanai_izvirzītās_lapas'): continue
		apivesture = do_api_req('lvwiki',onearticle)
		#rchanges = apivesture['query']["pages"]
		#theid = list(rchanges.keys())
		print('*'*60)
		pywikibot.output(onearticle)
		res = parse_one_article(onearticle,apivesture)
		if res:
			res.append(onearticle)
			sdf.append([res,apivesture])
	#
	#pywikibot.output(sdf)
	makeTable(sdf)
#
main()