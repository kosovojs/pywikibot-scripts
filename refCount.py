import pywikibot, re, os, requests, sys
import time
from datetime import timedelta, datetime

#os.chdir(r'projects/wpmed')
#jsub medRefs.sh

end2018 = datetime(2019, 1, 1, 0, 0, 1)
end2017 = datetime(2018, 1, 1, 0, 0, 1)
end2016 = datetime(2017, 1, 1, 0, 0, 1)

cite_regex = "{{\s*(?:[Tt]emplate\s*:)?\s*[Cc]ite"
refname_regex = "<\s*ref\s*name"
ref_regex = "<\s*ref\s*>"
ref1_regex = "<\s*ref"
pmid_regex = "\|\s*pmid\s*="
doi_regex = "\|\s*doi\s*="

wikilistarticles = eval(open('medicine2.txt','r', encoding='utf-8').read())

order = [['enwiki', 34516], ['dewiki', 10103], ['arwiki', 9855], ['frwiki', 8842], ['eswiki', 8296], ['itwiki', 7369], ['plwiki', 6988], ['ptwiki', 6737], ['ruwiki', 6423], ['jawiki', 5430], ['fawiki', 5307], ['nlwiki', 5125], ['zhwiki', 4815], ['svwiki', 4478], ['cawiki', 3976], ['ukwiki', 3833], ['srwiki', 3584], ['fiwiki', 3430], ['hewiki', 3253], ['cswiki', 2991], ['kowiki', 2839], ['shwiki', 2822], ['nowiki', 2558], ['trwiki', 2457], ['idwiki', 2412], ['viwiki', 2322], ['thwiki', 1971], ['simplewiki', 1884], ['huwiki', 1867], ['dawiki', 1864], ['rowiki', 1765], ['slwiki', 1676], ['glwiki', 1644], ['hrwiki', 1574], ['bgwiki', 1527], ['etwiki', 1515], ['euwiki', 1492], ['eowiki', 1433], ['hywiki', 1409], ['hiwiki', 1390], ['elwiki', 1315], ['tawiki', 1300], ['skwiki', 1161], ['cywiki', 1155], ['ltwiki', 1152], ['orwiki', 1143], ['kkwiki', 1127], ['mswiki', 1072], ['gawiki', 1031], ['azbwiki', 1024], ['azwiki', 948], ['bewiki', 924], ['mkwiki', 894], ['mlwiki', 835], ['lvwiki', 819], ['lawiki', 806], ['bswiki', 780], ['nnwiki', 745], ['bnwiki', 732], ['kywiki', 729], ['astwiki', 670], ['urwiki', 670], ['tlwiki', 635], ['uzwiki', 624], ['zh_yuewiki', 619], ['iswiki', 594], ['kawiki', 593], ['tewiki', 576], ['afwiki', 554], ['scowiki', 507], ['iowiki', 481], ['pawiki', 441], ['knwiki', 429], ['be_x_oldwiki', 410], ['sqwiki', 408], ['ckbwiki', 359], ['swwiki', 347], ['zh_min_nanwiki', 325], ['mrwiki', 315], ['dvwiki', 302], ['warwiki', 295], ['siwiki', 295], ['jvwiki', 293], ['ocwiki', 293], ['mywiki', 266], ['ttwiki', 246], ['newiki', 246], ['tgwiki', 227], ['pswiki', 214], ['fywiki', 214], ['lbwiki', 211], ['kuwiki', 207], ['yiwiki', 206], ['iawiki', 200], ['quwiki', 199], ['newwiki', 191], ['brwiki', 191], ['scnwiki', 188], ['suwiki', 178], ['wawiki', 173], ['pnbwiki', 170], ['ndswiki', 159], ['mnwiki', 151], ['wuuwiki', 151], ['alswiki', 149], ['arzwiki', 139], ['htwiki', 135], ['aswiki', 123], ['yowiki', 121], ['guwiki', 119], ['bawiki', 115], ['anwiki', 111], ['emlwiki', 104], ['sawiki', 104], ['liwiki', 103], ['cebwiki', 96], ['lnwiki', 93], ['sowiki', 88], ['sahwiki', 88], ['lmowiki', 84], ['mgwiki', 83], ['bat_smgwiki', 79], ['gdwiki', 79], ['diqwiki', 77], ['gnwiki', 77], ['sdwiki', 77], ['fowiki', 73], ['barwiki', 70], ['jamwiki', 70], ['ruewiki', 67], ['cvwiki', 66], ['xmfwiki', 66], ['amwiki', 65], ['tkwiki', 62], ['cdowiki', 60], ['hakwiki', 59], ['zh_classicalwiki', 58], ['pmswiki', 55], ['zawiki', 54], ['scwiki', 50], ['pamwiki', 47], ['snwiki', 47], ['ilowiki', 46], ['mznwiki', 45], ['bhwiki', 43], ['maiwiki', 43], ['csbwiki', 43], ['bxrwiki', 43], ['bowiki', 42], ['fiu_vrowiki', 40], ['frrwiki', 39], ['lgwiki', 39], ['lijwiki', 37], ['tyvwiki', 35], ['hifwiki', 34], ['aywiki', 34], ['extwiki', 34], ['vecwiki', 33], ['kmwiki', 33], ['kbpwiki', 33], ['rwwiki', 31], ['omwiki', 31], ['piwiki', 30], ['xhwiki', 29], ['bjnwiki', 28], ['ganwiki', 28], ['bclwiki', 27], ['arcwiki', 27], ['sewiki', 27], ['mwlwiki', 26], ['szlwiki', 26], ['nds_nlwiki', 24], ['gvwiki', 24], ['igwiki', 23], ['chrwiki', 22], ['vepwiki', 22], ['dinwiki', 22], ['oswiki', 21], ['roa_rupwiki', 21], ['dtywiki', 21], ['mtwiki', 21], ['nahwiki', 20], ['vlswiki', 20], ['cewiki', 19], ['kshwiki', 19], ['iuwiki', 18], ['lezwiki', 18], ['rnwiki', 18], ['nywiki', 18], ['napwiki', 18], ['tcywiki', 18], ['gomwiki', 18], ['lowiki', 18], ['tiwiki', 17], ['jbowiki', 17], ['furwiki', 17], ['sswiki', 16], ['cowiki', 16], ['ugwiki', 16], ['hawiki', 16], ['akwiki', 16], ['angwiki', 15], ['vowiki', 15], ['kaawiki', 15], ['nsowiki', 15], ['tswiki', 14], ['stwiki', 14], ['minwiki', 13], ['wowiki', 13], ['acewiki', 13], ['papwiki', 12], ['stqwiki', 12], ['novwiki', 11], ['mrjwiki', 11], ['mhrwiki', 11], ['nvwiki', 11], ['lbewiki', 10], ['hsbwiki', 10], ['bmwiki', 10], ['nrmwiki', 10], ['avwiki', 9], ['tnwiki', 9], ['map_bmswiki', 9], ['zeawiki', 9], ['bpywiki', 9], ['iewiki', 8], ['zuwiki', 8], ['kabwiki', 8], ['olowiki', 8], ['myvwiki', 8], ['kiwiki', 8], ['koiwiki', 8], ['kvwiki', 8], ['pcdwiki', 8], ['udmwiki', 7], ['ladwiki', 7], ['lrcwiki', 6], ['ikwiki', 6], ['hawwiki', 6], ['chywiki', 6], ['eewiki', 6], ['mdfwiki', 5], ['xalwiki', 5], ['pdcwiki', 5], ['krcwiki', 5], ['biwiki', 5], ['frpwiki', 5], ['cbk_zamwiki', 4], ['roa_tarawiki', 4], ['kwwiki', 4], ['glkwiki', 4], ['abwiki', 4], ['klwiki', 4], ['srnwiki', 4], ['miwiki', 3], ['pflwiki', 3], ['rmywiki', 3], ['pihwiki', 3], ['kswiki', 3], ['kbdwiki', 3], ['gotwiki', 3], ['vewiki', 2], ['towiki', 2], ['tpiwiki', 2], ['nawiki', 2], ['atjwiki', 2], ['kgwiki', 2], ['pagwiki', 2], ['rmwiki', 2], ['cuwiki', 2], ['smwiki', 1], ['gagwiki', 1], ['tumwiki', 1], ['tetwiki', 1], ['crhwiki', 1], ['dzwiki', 1], ['fjwiki', 1], ['ffwiki', 1], ['chwiki', 1], ['tywiki', 1], ['dsbwiki', 1]][::-1]

y2018 = open('refCount-2018-2.txt','a', encoding='utf-8')
notfound = open('refCount-2018-notfound-2.txt','a', encoding='utf-8')
'''
                    {
                        "revid": 2840508,
                        "parentid": 2840506,
                        "user": "Edgars2007",
                        "timestamp": "2018-04-15T08:05:08Z",
                        "comment": "Nov\u0113rsu izmai\u0146as, ko izdar\u012bja [[Special:Contributions/80.89.74.243|80.89.74.243]], atjaunoju versiju, ko saglab\u0101ja Pirags"
                    },
{
	"action": "query",
	"format": "json",
	"prop": "revisions",
	"titles": "Martins Dukurs",
	"rvprop": "timestamp|comment|user|ids",
	"rvlimit": "max",
	"rvdir": "older"
}

'''

def count_everything(text):
	text = re.sub(r'<!--.*?-->','',text)
	stats = {}
	cites = re.findall(cite_regex,text)
	refnames = re.findall(refname_regex,text)
	refs = re.findall(ref_regex,text)
	ref1s = re.findall(ref1_regex,text)
	pmids = re.findall(pmid_regex,text)
	dois = re.findall(doi_regex,text)
	
	stats.update({'cites':len(cites),
					'refnames':len(refnames),
					'refs':len(refs),
					'pmids':len(pmids),
					'dois':len(dois),
					'ref1s':len(ref1s)
	})
	
	return stats
#
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

def one_loop(wiki,article,revs,y18):
	for rev in revs:
		timest = rev["timestamp"]
		parsedtimest = datetime.strptime(timest,'%Y-%m-%dT%H:%M:%SZ')
		
		if not y18 and parsedtimest<end2018:
			y18 = True
			stats_out_content = count_everything(rev["*"])
			y2018.write('{}\t{}\t{}\t{}\n'.format(wiki,article,timest,stats_out_content))
			#break
			
		if y18:
			break
	
	return y18

def one_page_hist(title_check,wiki):
	try:
		apiout = do_api_req(wiki,title_check)#eval(open('dukursatsauces.json','r', encoding='utf-8').read())['query']
		
		rchanges = apiout['query']["pages"]
		theid = list(rchanges.keys())
		found2018 = False
		
		#counter = 0
		while (not found2018):
			#print(counter)
			#counter += 1
			do_ref_loop = one_loop(wiki,title_check,rchanges[theid[0]]['revisions'],found2018)
			found2018 = do_ref_loop
			
			if not found2018:
				if "continue" in apiout:
					contin_par = apiout["continue"]["rvcontinue"]
					apiout = do_api_req(wiki,title_check,contin_par)
					rchanges = apiout['query']["pages"]
				else:
					#print('fuck, no continue and no some data')
					notfound.write('{}\t{}\t{}\n'.format(wiki,title_check,'soem shit'))
					#notfound.append(title_check)
					break
			#print('State after loop: 17: {}, 16: {}'.format(found2017,found2016))
	except:
		notfound.write('{}\t{}\t{}\n'.format(wiki,title_check,'soem BIG shit'))
#



def main():
	print('Started at {}'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
	for wiki in order:
		wiki, articles = wiki
		if wiki not in wikilistarticles:
			notfound.write('{}\t{}\n'.format(wiki,'nav masiva'))
			continue
		print(wiki)
		print('Started this wiki at {}'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
		if not wiki.endswith('wiki') or wiki in ('commonswiki','wikidatawiki'): continue
		
		these_articles = wikilistarticles[wiki]
		print('{} articles'.format(len(these_articles)))
		
		counter = 0
		for one_article in these_articles:
			counter += 1
			if counter % 50 ==0:
				print(counter)
				sys.stdout.flush()
			one_page_hist(one_article,wiki)
		print('Ended this wiki at {}'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
	print('Done!!! at {}'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
	
	#these_articles = wikilistarticles['liwiki']
	
	#for one_article in these_articles:
	#	one_page_hist(one_article,'liwiki')
#
main()