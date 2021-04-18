import pywikibot, re, json, os, time, traceback
from datetime import datetime
import sqlite3 as lite
import sys

#os.chdir(r'projects/fide')
site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()


con = lite.connect(r'fide2.db')


#apr07datafile = eval(open('elobot-1-apr07-reals.txt', 'r', encoding='utf-8').read())

curtime = datetime.now()
#http://stackoverflow.com/questions/30071886/how-to-get-current-time-in-python-and-break-up-into-year-month-day-hour-minu
year,mon,day = [str(curtime.year), '{:0>2}'.format(str(curtime.month)), '{:0>2}'.format(str(curtime.day))]

def apicall(article='Q15397819'):
	r = pywikibot.data.api.Request(site=site, action='wbgetentities', format='json',
									ids=article, props='claims').submit()
									
	try:
		json_data = r['entities'][article]["claims"]
	except:
		return False
	#fsdfd = open('sdfsdfsdfsdfsdfs.txt', 'w', encoding='utf-8')
	#fsdfd.write(str(json_data))
	#itemlist = [blah['title'] for blah in json_data]
	
	return json_data#[0] if len(itemlist)>0 else False
#

#vars = [2551,2017,5,year,mon,day,12565]
#varr = [str(x) for x in vars]#tuple(map(str,vars))

def get_rang_hist(fide_id):
	#{'vals': {'feb17': '2402', 'may17': '2402', 'jan17': '2402', 'mar17': '2402', 'apr17': '2402'}, 'fide': '931179'}
	#try:
		#print('1')
		cur = con.cursor()
		#print('1')
		cur.execute('''select mon, rating from data where fide="{}" and mon like "2018-%"'''.format(fide_id))
		#print('1')
		data = cur.fetchall()
		#print(data)
		#print('1')
		data = {f[0]:f[1] for f in data}
		#print(data)
		#print('1')
		data = {'vals':data,'fide':fide_id}
		#print(data)
		#print('1')
		#print(data)
		
		return data
		#real_numbers = set([f[0] for f in data])
		#con.commit()

		#pywikibot.output(real_numbers[:50])
		#return real_numbers
		
	#finally:
	#	if con:
	#		con.close()
"""
1 - elo rangs
2 - year of rank
3 - mon of rank
4 - cur year
5 - cur mon
6 - cur day
7 - fide id
"""
def format_one_claim(vars):
	#vars = [2551,2017,'{:0>2}'.format(5),year,mon,day,12565]
	varr = [str(x) for x in vars]
	
	#rank = 'preferred' if varr[2]=='05' else 'normal'
	rank = 'normal'
	
	#iss piemers:
	#{"claims":[{"mainsnak":{"snaktype":"value","property":"P56","datavalue":{"value":"ExampleString","type":"string"}},"type":"statement","rank":"normal"}]}
	
	#{"mainsnak":{"snaktype":"value","property":"P1087","datavalue":{"value":{"amount": "+2851","unit": "1"},"type": "quantity"},"datatype": "quantity"},"type":"statement","rank":"normal","qualifiers": {"P585": [{"snaktype": "value","property": "P585","datavalue": {"value": {"time": "+2016-05-01T00:00:00Z","timezone": 0,"before": 0,"after": 0,"precision": 10,"calendarmodel": "http://www.wikidata.org/entity/Q1985727"},"type": "time"},"datatype": "time"}]},"qualifiers-order": ["P585"],"references": [{"snaks": {"P248": [{"snaktype": "value","property": "P248","datavalue": {"value": {"entity-type": "item","id": "Q27038151"},"type": "wikibase-entityid"},"datatype": "wikibase-item"}],"P813": [{"snaktype": "value","property": "P813","datavalue": {"value": {"time": "+2016-09-21T00:00:00Z","timezone": 0,"before": 0,"after": 0,"precision": 11,"calendarmodel": "http://www.wikidata.org/entity/Q1985727"},"type": "time"},"datatype": "time"}],"P1440": [{"snaktype": "value","property": "P1440","datavalue": {"value": "1503014","type": "string"},"datatype": "external-id"}]},"snaks-order": ["P248","P813","P1440"]}]}
	
	oneclaim = '{"mainsnak":{"snaktype":"value","property":"P1087","datavalue":{"value":{"amount": "+' + varr[0] + '","unit": "1"},"type": "quantity"},"datatype": "quantity"},"type":"statement","rank":"' + rank + '","qualifiers": {"P585": [{"snaktype": "value","property": "P585","datavalue": {"value": {"time": "+' + varr[1] + '-' + varr[2] + '-01T00:00:00Z","timezone": 0,"before": 0,"after": 0,"precision": 10,"calendarmodel": "http://www.wikidata.org/entity/Q1985727"},"type": "time"},"datatype": "time"}]},"qualifiers-order": ["P585"],"references": [{"snaks": {"P248": [{"snaktype": "value","property": "P248","datavalue": {"value": {"entity-type": "item","id": "Q27038151"},"type": "wikibase-entityid"},"datatype": "wikibase-item"}],"P813": [{"snaktype": "value","property": "P813","datavalue": {"value": {"time": "+' + varr[3] + '-' + varr[4] + '-' + varr[5] + 'T00:00:00Z","timezone": 0,"before": 0,"after": 0,"precision": 11,"calendarmodel": "http://www.wikidata.org/entity/Q1985727"},"type": "time"},"datatype": "time"}],"P1440": [{"snaktype": "value","property": "P1440","datavalue": {"value": "' + varr[6] + '","type": "string"},"datatype": "external-id"}]},"snaks-order": ["P248","P813","P1440"]}]}'
	

	#pywikibot.output(oneclaim)
	
	return eval(oneclaim)
#
#format_one_claim()

jfffff = """{"claims":[                    {
                        "mainsnak": {
                            "snaktype": "value",
                            "property": "P1087",
                            "datavalue": {
                                "value": {
                                    "amount": "+2872",
                                    "unit": "1",
                                    "upperBound": "+2872",
                                    "lowerBound": "+2872"
                                },
                                "type": "quantity"
                            },
                            "datatype": "quantity"
                        },
                        "type": "statement",
                        "qualifiers": {
                            "P585": [
                                {
                                    "snaktype": "value",
                                    "property": "P585",
                                    "datavalue": {
                                        "value": {
                                            "time": "+2013-09-01T00:00:00Z",
                                            "timezone": 0,
                                            "before": 0,
                                            "after": 0,
                                            "precision": 10,
                                            "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                                        },
                                        "type": "time"
                                    },
                                    "datatype": "time"
                                }
                            ]
                        },
                        "qualifiers-order": [
                            "P585"
                        ],
                        "rank": "normal",
                        "references": [
                            {
                                "snaks": {
                                    "P813": [
                                        {
                                            "snaktype": "value",
                                            "property": "P813",
                                            "datavalue": {
                                                "value": {
                                                    "time": "+2016-09-21T00:00:00Z",
                                                    "timezone": 0,
                                                    "before": 0,
                                                    "after": 0,
                                                    "precision": 11,
                                                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                                                },
                                                "type": "time"
                                            },
                                            "datatype": "time"
                                        }
                                    ],
                                    "P1440": [
                                        {
                                            "snaktype": "value",
                                            "property": "P1440",
                                            "datavalue": {
                                                "value": "1503014",
                                                "type": "string"
                                            },
                                            "datatype": "external-id"
                                        }
                                    ],
                                    "P248": [
                                        {
                                            "snaktype": "value",
                                            "property": "P248",
                                            "datavalue": {
                                                "value": {
                                                    "entity-type": "item",
                                                    "numeric-id": 27038151,
                                                    "id": "Q27038151"
                                                },
                                                "type": "wikibase-entityid"
                                            },
                                            "datatype": "wikibase-item"
                                        }
                                    ]
                                },
                                "snaks-order": [
                                    "P813",
                                    "P1440",
                                    "P248"
                                ]
                            }
                        ]
                    },
					                    {
                        "mainsnak": {
                            "snaktype": "value",
                            "property": "P1087",
                            "datavalue": {
                                "value": {
                                    "amount": "+2872",
                                    "unit": "1",
                                    "upperBound": "+2872",
                                    "lowerBound": "+2872"
                                },
                                "type": "quantity"
                            },
                            "datatype": "quantity"
                        },
                        "type": "statement",
                        "qualifiers": {
                            "P585": [
                                {
                                    "snaktype": "value",
                                    "property": "P585",
                                    "datavalue": {
                                        "value": {
                                            "time": "+2013-05-01T00:00:00Z",
                                            "timezone": 0,
                                            "before": 0,
                                            "after": 0,
                                            "precision": 10,
                                            "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                                        },
                                        "type": "time"
                                    },
                                    "datatype": "time"
                                }
                            ]
                        },
                        "qualifiers-order": [
                            "P585"
                        ],
                        "rank": "preferred",
                        "references": [
                            {
                                "snaks": {
                                    "P813": [
                                        {
                                            "snaktype": "value",
                                            "property": "P813",
                                            "datavalue": {
                                                "value": {
                                                    "time": "+2016-11-21T00:00:00Z",
                                                    "timezone": 0,
                                                    "before": 0,
                                                    "after": 0,
                                                    "precision": 11,
                                                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                                                },
                                                "type": "time"
                                            },
                                            "datatype": "time"
                                        }
                                    ],
                                    "P1440": [
                                        {
                                            "snaktype": "value",
                                            "property": "P1440",
                                            "datavalue": {
                                                "value": "1503014",
                                                "type": "string"
                                            },
                                            "datatype": "external-id"
                                        }
                                    ],
                                    "P248": [
                                        {
                                            "snaktype": "value",
                                            "property": "P248",
                                            "datavalue": {
                                                "value": {
                                                    "entity-type": "item",
                                                    "numeric-id": 27038151,
                                                    "id": "Q27038151"
                                                },
                                                "type": "wikibase-entityid"
                                            },
                                            "datatype": "wikibase-item"
                                        }
                                    ]
                                },
                                "snaks-order": [
                                    "P813",
                                    "P1440",
                                    "P248"
                                ]
                            }
                        ]
                    }]}
"""
def removekey(d, key):
	r = dict(d)
	del r[key]
	return r
#

convvv = {
	'feb17':'02-17',
	'may17':'05-17',
	'jan17':'01-17',
	'mar17':'03-17',
	'apr17':'04-17'
}

def addclaims(item,data,alreadymonths):
	#{'vals': {'feb17': '2402', 'may17': '2402', 'jan17': '2402', 'mar17': '2402', 'apr17': '2402'}, 'fide': '931179'}
	fideid = data['fide']
	data1 = data['vals']#{'02-17': '2838', '04-17': '2838', '05-17': '2832', '03-17': '2838'}
	alreadymonths = [f.replace('-01T00:00:00Z','').replace('+','') for f in alreadymonths]#+2013-09-01T00:00:00Z
	
	toaddwd = []
	summary = []
	
	#orderlist = ['jan17','feb17','mar17','apr17','may17']
	
	for entr in data1:
		if entr in alreadymonths:
			continue
			
		elo = data1[entr]
		#sdfdsdf = convvv[entr]
		
		rankyear,rankmon = entr.split('-')
		
		vars = [elo,'{}'.format(rankyear),'{:0>2}'.format(rankmon),year,mon,day,fideid]
		gfdgfdfgdfgf = format_one_claim(vars)
		toaddwd.append(gfdgfdfgdfgf)
		summary.append(entr)
	#
	return toaddwd,summary
	

def do_ranks_bounds(thisitem,json):
	summary = []
	#if 
	
	json = json['P1087']#eval(json)['P1087']#["claims"]
	for cl in json:
		if cl['rank']=='preferred':
			summary.append('changed rank to "normal"')
			cl['rank']='normal'
			
		#apr07 fix
		try:
			date = cl['qualifiers']['P585'][0]['datavalue']['value']['time']
			
		
			if date=='+2007-04-01T00:00:00Z':
				if thisitem in apr07datafile:
					realval = ''
					realval = '+{}'.format(apr07datafile[thisitem])
					cl['mainsnak']['datavalue']['value']['amount'] = realval
					summary.append('fixed April 2007 rating')
		except KeyError:
			print('no qualifier')
		
		#do bounds
		boundscheck = cl['mainsnak']['datavalue']['value']
		
		if "upperBound" in boundscheck or "lowerBound" in boundscheck:
			newcl = {}
			newcl.update({"unit":boundscheck["unit"],"amount":boundscheck["amount"]})
			cl['mainsnak']['datavalue']['value'] = newcl
			summary.append('removed ±0 bounds')
		
		#if "upperBound" in boundscheck:
		#	cl = removekey(cl['mainsnak']['datavalue']['value'],"upperBound")
		#if "lowerBound" in boundscheck:
		#	cl = removekey(cl['mainsnak']['datavalue']['value'],"lowerBound")
			
	#pywikibot.output(json)		
	
	#fsdfdfdfsddsa = open('sdfsdfsdfsdsfdssdfsdfsdfsfsdfsfsdf.txt', 'w', encoding='utf-8')
	#fsdfdfdfsddsa.write(str(json))
	return json,summary
#
def do_ranks_boundsOLD(json):
	summary = []
	#if 
	
	json = json['P1087']#eval(json)['P1087']#["claims"]
	for cl in json:
		if cl['rank']=='preferred':
			summary.append('changed rank to "normal"')
			cl['rank']='normal'
			
		#do bounds
		boundscheck = cl['mainsnak']['datavalue']['value']
		
		if "upperBound" in boundscheck or "lowerBound" in boundscheck:
			newcl = {}
			newcl.update({"unit":boundscheck["unit"],"amount":boundscheck["amount"]})
			cl['mainsnak']['datavalue']['value'] = newcl
			summary.append('removed ±0 bounds')
		
		#if "upperBound" in boundscheck:
		#	cl = removekey(cl['mainsnak']['datavalue']['value'],"upperBound")
		#if "lowerBound" in boundscheck:
		#	cl = removekey(cl['mainsnak']['datavalue']['value'],"lowerBound")
			
	#pywikibot.output(json)		
	
	#fsdfdfdfsddsa = open('sdfsdfsdfsdsfdssdfsdfsdfsfsdfsfsdf.txt', 'w', encoding='utf-8')
	#fsdfdfdfsddsa.write(str(json))
	return json,summary


#do_ranks_bounds(jfffff)

def do_one_item(item,itemdata):
	#item = 'Q15397819'
	#try:
		apires = apicall(item)#open('sdfsdfsdfsdfsdfs.txt', 'r', encoding='utf-8').read()#apicall(item)
		
		if not apires:
			put_data_in_db(item,'error')
			return 0

		if 'P1087' in apires:
			months_already = [f["qualifiers"]["P585"][0]["datavalue"]["value"]["time"] for f in apires['P1087']]
		else:
			months_already = []

		Qitem = pywikibot.ItemPage(repo, item)
		Qitem.get()
		'''
		if 'P1087' in apires:

			for_boundrem,boudsumm = do_ranks_bounds(item,apires)

			if len(boudsumm)>0:
				summary_bounds = '[[Property:P1087]] clean-up: {}'.format(', '.join(list(set(boudsumm))))
			
				sdfsdfsdfdasdas = {"claims":{"P1087":for_boundrem}}
			
				Qitem.editEntity(json.loads(json.dumps(sdfsdfsdfdasdas)), summary=summary_bounds)
		'''
		claimadding, clsumm = addclaims(item,itemdata,months_already)

		if len(clsumm)>0:
			clsumm.sort()
			summary_newcl = 'Added new [[Property:P1087]] values: {}'.format(', '.join(clsumm))
			
			sdfsdfsdf = {"claims":claimadding}
			
			#fsdfddsa = open('sdfsdfsdfsdfsdfsfsdfsfsdf.txt', 'w', encoding='utf-8')
			#fsdfddsa.write(str(sdfsdfsdf))
			#fsdfddsa.write(str(json.loads(json.dumps(str(sdfsdfsdf)))))
			Qitem.editEntity(json.loads(json.dumps(sdfsdfsdf)), summary=summary_newcl)
			put_data_in_db(item)
	#except:
	#	print('Got exception: {}'.format(item))
	#	put_data_in_db(item,'exception')
#
def get_info_from_db():
	cur = con.cursor()
	cur.execute('''select wd, fide from meta where timestamp is null limit 1''')
	data = cur.fetchall()
	if len(data)>0:
		data = data[0]
		return data
	else:
		return False
	#print(data)
	
def put_data_in_db(wditem,info=''):
	cur = con.cursor()
	if info!='':
		toput = info
	else:
		toput = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	cur.execute('''UPDATE meta SET timestamp="{}" WHERE wd = "{}"'''.format(toput,wditem))
	con.commit()
#

def main():
	hasmoredata = True
	counter = 0
	begintime = time.time()
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	while hasmoredata:
		#try:
			infodata = get_info_from_db()
			if not infodata:
				hasmoredata = False
				break
			
			counter += 1
			if counter % 50 == 0:
				print('\t\t'+str(counter))
				sys.stdout.flush()
			
			#if counter==5:
			#	hasmoredata = False
				
			item,fideId = infodata
			#print(item)
			ranghist = get_rang_hist(fideId)
			do_one_item(item,ranghist)
			time.sleep(2)
		#except:
		#	print('final except')
			#pywikibot.output(traceback.format_exc())
		#	hasmoredata = False
	#
	con.close()
	print('Done!')
	endtime = time.time()
	print('it took: {}'.format((endtime-begintime)))
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		
		
	
#
def mainOOOLLLD():
	#txtdata = eval(open('elobot-2.txt', 'r', encoding='utf-8').read())
	#blacklist = open('elobot-blacklist.txt', 'r', encoding='utf-8').read().split('\n')
	
	#print(len(txtdata))
	
	counter = 0
	for itemdata in txtdata:
		counter += 1
		item,data = itemdata
		print(item)
		if counter % 50 == 0:
			print('\t\t'+str(counter))
			
		if item in blacklist:
			continue
		
		do_one_item(item,data)
	
	
#
main()