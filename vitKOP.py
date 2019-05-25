import requests
import pywikibot
import json, os, sys
import urllib.parse

#os.chdir(r'projects/vital')

#nākamajām reizēm - ielikt vēl kaut kādus rādītājus - lielāko/mazāko
#salikt pa mēnešiem

null = ''
articles = eval(open("quarry-29111-vital-views-run284581.json", "r", encoding='utf-8').read())['rows']
#articles = [[f[0],f[1],f[2],f[3],f[4]] for f in articles]
#pywikibot.output(articles)

def oneArticle(wiki,article):
	#pywikibot.output(urllib.parse.quote(article))
	urltoopen = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{}.wikipedia/all-access/user/{}/daily/20150901/20180817'.format(wiki,urllib.parse.quote(article))
	res = requests.get(urltoopen).json()
	
	#data1 = json.loads(res)
	
	if 'items' in res:
		dict1 = [article1['views'] for article1 in res['items']]
	else:
		dict1 = [0]
	
	joined = [str(sfsf) for sfsf in dict1]
	
	#pywikibot.output(dict1)
	#pywikibot.output(sum(dict1))
	#pywikibot.output(len(dict1))
	
	outputstr = "{}\t{}\t{}\t{}\t{}".format(wiki,article,str(sum(dict1)),str(len(dict1)),str('|'.join(joined)))
	
	return outputstr
	
mapping = {
	0:'en',
	1:'de',
	2:'ru',
	3:'pl',
	4:'fr',
	5:'es',
}
# and open("file2-vitals-kop.txt", "w", encoding='utf-8') as openedfile2
def main():
	with open("vitals v1 vvvvvvvvvv nr656546451111.txt", "w", encoding='utf-8') as openedfile:
		counter = 0
		for article in articles:
			#pywikibot.output('')
			#pywikibot.output(article)
			counter += 1
			if counter % 25 == 0:
				print(counter)
				sys.stdout.flush()
			for lang in mapping:
				
				
				
				articletocheck = article[lang]
				#pywikibot.output(articletocheck)
				langtocheck = mapping[lang]
				#pywikibot.output(langtocheck)
				if articletocheck!=None:
					
					sfdsfd = oneArticle(langtocheck,articletocheck)
					openedfile.write(article[0]+'\t'+str(sfdsfd)+'\n')
	print('Done')
	
main()