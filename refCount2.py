import pywikibot, re, os, requests, sys
import time
from datetime import timedelta, datetime

#os.chdir(r'projects/wpmed')
#jsub medRefs.sh

end2017 = datetime(2018, 1, 1, 0, 0, 1)
end2016 = datetime(2017, 1, 1, 0, 0, 1)

cite_regex = "{{\s*(?:[Tt]emplate\s*:)?\s*[Cc]ite"
refname_regex = "<\s*ref\s*name"
ref_regex = "<\s*ref\s*>"
ref1_regex = "<\s*ref"
pmid_regex = "\|\s*pmid\s*="
doi_regex = "\|\s*doi\s*="

wikilistarticles = open('refCount-notfound-2.txt','r', encoding='utf-8').read()
wikilistarticles = [f.split('\t') for f in  wikilistarticles.split('\n') if len(f)>3]

order = '''enwiki	32262
dewiki	9762
arwiki	8686
frwiki	8529
eswiki	7889
itwiki	7112
plwiki	6762
ptwiki	6465'''
order = [f.split('\t')[0] for f in order.split('\n') if len(f)>3][::-1]

y2017 = open('refCount-2017-3.txt','a', encoding='utf-8')
y2016 = open('refCount-2016-3.txt','a', encoding='utf-8')
notfound = open('refCount-notfound-3.txt','a', encoding='utf-8')
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

def one_loop(wiki,article,revs,y17,y16):
	for rev in revs:
		timest = rev["timestamp"]
		parsedtimest = datetime.strptime(timest,'%Y-%m-%dT%H:%M:%SZ')
		
		if not y17 and parsedtimest<end2017:
			y17 = True
			stats_out_content = count_everything(rev["*"])
			y2017.write('{}\t{}\t{}\t{}\n'.format(wiki,article,timest,stats_out_content))
			#break
			
		if not y16 and parsedtimest<end2016:
			y16 = True
			stats_out_content = count_everything(rev["*"])
			y2016.write('{}\t{}\t{}\t{}\n'.format(wiki,article,timest,stats_out_content))
		
		if y17 and y16:
			break
	
	return (y17,y16)

def one_page_hist(title_check,wiki):
	try:
		apiout = do_api_req(wiki,title_check)#eval(open('dukursatsauces.json','r', encoding='utf-8').read())['query']
		
		rchanges = apiout['query']["pages"]
		theid = list(rchanges.keys())
		found2017 = False
		found2016 = False
		
		#counter = 0
		while (not found2017 or not found2016):
			#print(counter)
			#counter += 1
			do_ref_loop = one_loop(wiki,title_check,rchanges[theid[0]]['revisions'],found2017,found2016)
			found2017 = do_ref_loop[0]
			found2016 = do_ref_loop[1]
			
			if not found2017 or not found2016:
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
	print('{} articles'.format(len(wikilistarticles)))
	
	counter = 0
	for entry in wikilistarticles:
		wikipr,article,_ = entry
		counter += 1
		if counter % 50 ==0:
			print(counter)
			sys.stdout.flush()
		one_page_hist(article,wikipr)
	print('Done!!! at {}'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
	
	#these_articles = wikilistarticles['liwiki']
	
	#for one_article in these_articles:
	#	one_page_hist(one_article,'liwiki')
#
main()