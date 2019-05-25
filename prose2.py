import re, pywikibot, os
from bs4 import BeautifulSoup, Tag


#os.chdir(r'projects/cee')

site = pywikibot.Site("lv", "wikipedia")

apiq = '''{
	"action": "parse",
	"format": "json",
	"page": "Diāna Hadžijeva",
	"prop": "text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings"
}'''

def get_prose(apiresult):
	#http://stackoverflow.com/questions/40052116/how-to-remove-html-tags-in-beautifulsoup-when-i-have-contents
	#http://stackoverflow.com/questions/18453176/removing-all-html-tags-along-with-their-content-from-text
	soup = BeautifulSoup(apiresult, "html.parser")

	for tag in soup.find_all('table'):
		tag.replaceWith('')

	for tag in soup.find_all('span',{'class':'noexcerpt'}):
		tag.replaceWith('')

	for tag in soup.find_all('span',{'class':'mw-editsection'}):
		tag.replaceWith('')

	for tag in soup.find_all('ol',{'class':'references'}):
		tag.replaceWith('')

	for tag in soup.find_all('h2'):
		tag.replaceWith('')

	for tag in soup.find_all('h3'):
		tag.replaceWith('')

	for tag in soup.find_all('h4'):
		tag.replaceWith('')
	
	
#
	thistext = str(soup.get_text()).strip('\s\n')
	thistext = thistext.replace('\n','')
	#pywikibot.output('---{}-----'.format(thistext))
	#print(len(thistext))
	
	return len(thistext)

def do_api(article):
	
	r = pywikibot.data.api.Request(site=site, action='parse', format='json',
									page=article, prop='text').submit()
									
	json_data = r['parse']['text']['*']
	
	return json_data


def main():
	fileop = eval(open('cee-all-articles.txt', 'r', encoding='utf-8').read())
	fileop2 = open('ceeraksti-prose2.txt', 'w', encoding='utf-8')
	
	alreadyhave = eval(open('ceeraksti-prose22.txt', 'r', encoding='utf-8').read())
	
	
	fileop22 = open('ceeraksti-prose22.txt', 'w', encoding='utf-8')
	
	articles = [f[0] for f in fileop if f[0] not in alreadyhave]
	print(len(articles))
	
	gdfdf = {}
	gdfdf2 = {}
	
	gdfdf2.update(alreadyhave)
	
	for article in articles:
		#pywikibot.output(article)
		apires = do_api(article)
		gdfdf.update({article:apires})
		reslen = get_prose(apires)
		gdfdf2.update({article:reslen})
		#print(reslen)
	fileop2.write(str(gdfdf))
	fileop22.write(str(gdfdf2))
	print('done')
#
main()