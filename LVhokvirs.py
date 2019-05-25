import requests, json, pywikibot, re, os, datetime
from bs4 import BeautifulSoup

#os.chdir(r'projects/sportsTables')

site = pywikibot.Site('lv', 'wikipedia')
article = '2018.—2019. gada Optibet hokeja līgas sezona'

#input = open('new.html','r', encoding='utf-8').read()

team_mapping = {
	'HK Prizma': 'PRI',
	'HK Kurbads': 'KUR',
	'HS Rīga': 'RIG',
	'HK Zemgale/LLU': 'LLU',
	'HK MOGO': 'MOG',
	'HK Liepāja': 'LIE',
	'HK Lido': 'LID'
}

#url = 'http://stats.lhf.lv/2016_2017_latvijas_virsligas_hokeja_cempionats/'
#res = requests.get(url)
#soup = BeautifulSoup(res.text, "html.parser")

dict = {}

reslist = []

today = datetime.date.today()

def dooutput(teams,res):
	teamLIST = teamlist2
	updatedate = today.strftime('{{dat|%Y|%m|%d||bez}}')
	wikitext = '''{{#invoke:Sporta tabula|main\n|source= \n\n|template_name=''' + tlname + '''\n''' + teams + '''\n''' + res + '''\n''' + teamLIST + '''\n}}<noinclude>\n[[Kategorija:Vikipēdijas veidnes]]\n</noinclude>'''
	
	return wikitext
#
def makeTable():
	url = 'https://lhf.lv/lv/subtournament/294'
	res = requests.get(url)

	soup = BeautifulSoup(res.text, "html.parser")

	divTag = soup.find('div',{'class':'teams-tab'})
	if not divTag:
		return None
	theTable = divTag.find('table',{'class':'stats'}).tbody
	
	for team in theTable.findAll('tr',{'class':'expandable-row'}):
		data = team.findAll('td')
		place = int(data[0].text.strip())
		name = data[1].text.strip()
		wins = data[4].text.strip()
		winsOT = data[5].text.strip()
		lossesOT = data[6].text.strip()
		losses = data[7].text.strip()
		goals = data[8].text.strip()
		goalsfor,goalsag = goals.split(':')
		
		teamname = team_mapping[name]
		
		#pywikibot.output("\t".join([name,win,winOT,lossOT,loss,goals]))
		
		string = '|win_' + teamname + '=' + wins + ' |OTwin_' + teamname + '=' + winsOT + ' |OTloss_' + teamname + '=' + lossesOT + ' |loss_' + teamname + '=' + losses + ' |gf_' + teamname + '=' + goalsfor + '|ga_' + teamname + '=' + goalsag
		reslist.append(string)
		dict.update({place:teamname})
	#
	c = []
	for i in dict:
		c.append('|team'+str(i)+'='+dict[i])

	teamlist = ' '.join(c)
	results = '\n'.join(reslist)

	wikitext = '''{{#invoke:Sporta tabula|main|style=WL OT
|source=[https://lhf.lv/lv/subtournament/294 LHF]
|OTwin_header={{Abbr|OTW|Uzvara pagarinājumā vai pēcspēles metienos}} |OTloss_header={{Abbr|OTL|Zaudējums pagarinājumā vai pēcspēles metienos}}

''' + teamlist + '''

''' + results + '''

|name_PRI=[[HK Prizma]]
|name_KUR=[[HK Kurbads]]
|name_RIG=[[HS Rīga]]
|name_LLU=[[HK Zemgale/LLU]]
|name_MOG=[[HK MOGO]]
|name_LIE=[[HK Liepāja]]
|name_LID=[[HS Lido]]
}}'''
	
	return wikitext

def getCurrent(lvtext):
	currText = re.search('<!-- TABLE START -->\n(.*)\n<!-- TABLE END -->',lvtext, flags=re.DOTALL)
	
	if currText:
		return currText.group(1)
	
	return False


def doreplace(text,pretext,header,footer):
	newtext = re.sub(header + '.*' + footer, header + '\n' + pretext + '\n' + footer, text, flags=re.DOTALL)
	#pywikibot.output(newtext)
	
	return newtext
#
def main():
	thepage = pywikibot.Page(site, article)
	lvtext = thepage.get()
	
	currenttext = getCurrent(lvtext)
	#pywikibot.output(currenttext)
	
	if not currenttext: return 0#paziņot man
	
	newTable = makeTable()
	
	#pywikibot.output(newTable)
	
	if newTable and newTable!=currenttext:
		tableInserted = doreplace(lvtext,newTable,'<!-- TABLE START -->','<!-- TABLE END -->')
		
		thepage.text = tableInserted
		thepage.save(comment='Bots: atjaunināta tabula', botflag=True)
	else:
		print('no changes')
	
#
main()