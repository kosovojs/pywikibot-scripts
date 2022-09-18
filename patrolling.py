import pywikibot, os, re, requests
from pywikibot.data import api
from datetime import timedelta, datetime

start = datetime.today() - timedelta(minutes=65)
starttime = start.strftime('%Y-%m-%dT%H:%M:%S.000Z')#start.strftime('%Y%m%d%H%M%S')

#2018-05-06T08:13:37.000Z
#print(starttime)

site = pywikibot.Site('lv', 'wikipedia')
#site.login()

revert_regex = 'izdarīto izmaiņu (\d+)'

#os.chdir(r'projects/lv')

#rchanges = eval(open('fake_rc.json','r', encoding='utf-8').read())['query']["recentchanges"]

#Atc\u0113lu [[Special:Contributions/Lieeeneee|Lieeeneee]] ([[User talk:Lieeeneee|diskusija]]) izdar\u012bto izmai\u0146u 2852257

file1 = open('patrollog_undone.txt','a', encoding='utf-8')
file2 = open('patrollog_undone1.txt','a', encoding='utf-8')

def get_username(text):
	reg = 'Dalībnie[^:]+:([^\/]+).*?'
	res = re.search(reg,text)
	if res:
		return res.group(1)

	return False

def get_rc():
	params = {
		"action": "query",
		"format": "json",
		"list": "recentchanges",
		"rcend": starttime,
		"rcdir": "older",
		"rcprop": "title|timestamp|ids|user|comment|flags|loginfo|tags|patrolled",
		"rclimit": "max",
		"rctype": "edit|new"
	}

	#https://lv.wikipedia.org/w/api.php?action=query&format=json&list=recentchanges&rcprop=title|timestamp|ids|user|comment|flags|loginfo|tags|patrolled&rclimit=500&rctype=edit|new&rcend=2018-05-06T11:56:58.000Z&rcdir=older


	req = api.Request(site=site, parameters=params)
	data = req.submit()

	#r = requests.get('https://lv.wikipedia.org/w/api.php?',params = params)
	#r.encoding = 'utf-8'
	#json_data = eval(r.text)
	#pywikibot.output(data['query']["recentchanges"])

	return data['query']["recentchanges"]
#

rchanges = get_rc()

#for change in site.recentchanges(start=starttime, showBot=False, showPatrolled=True, reverse=True):
for change in rchanges:
	#{"type":"edit","ns":0,"title":"Valsts aizsarg\u0101jamie kult\u016bras pieminek\u013ci Raunas novad\u0101","pageid":244221,"revid":2852438,"old_revid":2852435,"rcid":7642203,"user":"VollBot","bot":"","minor":"","timestamp":"2018-05-06T08:25:34Z","comment":"Added wikidata item to list...","patrolled":"","autopatrolled":"","tags":[]}
	#pywikibot.output(change)
	try:
		summary = change["comment"] if "comment" in change else ''

		if summary.startswith('Atcēlu '):
			sdfsdfsfd = re.search(revert_regex,summary)
			if sdfsdfsfd:
				theedittopatrol = sdfsdfsfd.group(1)
				pywikibot.output('Patrolling undone: {}'.format(theedittopatrol))
				file1.write('Undone\t{}\t{}\t{}\tFrom: {}\tRevert user: {}\n'.format(theedittopatrol,change['title'],summary,change['revid'],change['user']))
				p = site.patrol(revid=int(theedittopatrol))
				next(p)
				#patrol_edit(int(theedittopatrol))



		if 'unpatrolled' not in change: continue

		if change['ns']==4 and change['title']=='Vikipēdija:Smilšu kaste':
			#do patrol
			pywikibot.output('Patrolling: {}'.format(change["revid"]))
			file2.write('{}\n'.format(change["revid"]))
			p = site.patrol(revid=change['revid'])
			next(p)
		#
		if 'Commons:Commons:GlobalReplace' in summary:
			pywikibot.output('Patrolling: {}'.format(change["revid"]))
			file2.write('{}\n'.format(change["revid"]))
			p = site.patrol(revid=change['revid'])
			next(p)


		if change['ns'] in (2,3) and get_username(change['title'])==change["user"]:
			#do patrol
			pywikibot.output('Patrolling: {}'.format(change["revid"]))
			file2.write('{}\n'.format(change["revid"]))
			p = site.patrol(revid=change['revid'])
			next(p)
	except pywikibot.exceptions.Error:
		continue
