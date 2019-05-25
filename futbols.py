import requests, json, pywikibot, re, os, datetime
from bs4 import BeautifulSoup

site = pywikibot.Site('lv', 'wikipedia')
article = '2019. gada Latvijas futbola Virslīgas sezona'

team_mapping = {
	'RFS': 'RFS',
	'Riga FC': 'RFC',
	'Valmiera Glass ViA': 'VAL',
	'FK Ventspils': 'VEN',
	'FK Jelgava': 'JEL',
	'FK Liepāja': 'LIEP',
	'BFC Daugavpils': 'BFC',
	'FK Metta': 'MET',
	'FK Spartaks': 'SPA'
}


headers = {
    'User-Agent': u'Vikipēdijas robots tabulas datu atjaunināšanai (kosovojs@gmail.com)'.encode('utf-8')
}

#url = 'http://stats.lhf.lv/2016_2017_latvijas_virsligas_hokeja_cempionats/'
#res = requests.get(url)
#soup = BeautifulSoup(res.text, "html.parser")

dict = {}

reslist = []

today = datetime.date.today()

def makeTable():
	url = 'https://lff.lv/sacensibas/viriesi/optibet-virsliga/'
	res = requests.get(url, headers=headers)
	res.encoding = 'utf-8'

	#res = input

	forSoup = res.text

	#with open('aaa.txt',mode='w',encoding='UTF-8') as fileS:
	#	fileS.write(forSoup)

	soup = BeautifulSoup(forSoup, "html.parser")

	#print(soup)
	theTable = soup.find('table',{'class':'rankings'})


	allRows = theTable.findAll('tr')
	
	#<th>Komanda</th><th>S</th><th>U</th><th>N</th><th>Z</th><th class="gr">GV</th><th class="gr2">ZV</th><th class="gr">VA</th><th>P</th>
	for team in allRows[1:]:
		data = team.findAll('td')
		place = int(data[0].text.strip())
		name = data[1].text.strip()
		wins = data[3].text.strip()
		neizskirti = data[4].text.strip()
		losses = data[5].text.strip()
		goalsfor = data[6].text.strip()
		goalsag = data[7].text.strip()
		
		teamname = team_mapping[name]
		
		#pywikibot.output("\t".join([name,win,winOT,lossOT,loss,goals]))
		
		#|win_Liep=15 |draw_Liep=6 |loss_Liep=7 |gf_Liep=46 |ga_Liep=25
		string = '|win_' + teamname + '=' + wins + ' |draw_' + teamname + '=' + neizskirti + ' |loss_' + teamname + '=' + losses + ' |gf_' + teamname + '=' + goalsfor + '|ga_' + teamname + '=' + goalsag
		reslist.append(string)
		dict.update({place:teamname})
	#
	c = []
	for i in dict:
		c.append('|team'+str(i)+'='+dict[i])

	teamlist = ' '.join(c)
	results = '\n'.join(reslist)

	wikitext = '''{{#invoke:Sporta tabula|main|style=WDL
|source=[https://lff.lv/sacensibas/viriesi/optibet-virsliga/ LFF]

''' + teamlist + '''

''' + results + '''

|name_RFS=[[RFS]]
|name_RFC=[[Riga FC]]
|name_VAL=[[Valmiera Glass VIA]]
|name_VEN=[[FK Ventspils]]
|name_JEL=[[FK Jelgava]]
|name_LIEP=[[FK Liepāja]]
|name_BFC=[[BFC Daugavpils]]
|name_MET=[[FS METTA/Latvijas Universitāte|METTA/LU]]
|name_SPA=[[FK Spartaks Jūrmala|FK Spartaks]]

|result1=ČL |result2=EL |result3=EL |result9=PR

|res_col_header=QR
|col_ČL=green1 |text_ČL=2019.—2020. gada [[UEFA Čempionu līga]]s 1. kvalifikācijas kārta
|col_EL=blue1 |text_EL=2019.—2020. gada [[UEFA Eiropas līga]]s 1. kvalifikācijas kārta
|col_PR=red2 |text_PR=Pārspēles par palikšanu Virslīgā
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
	
	#if not currenttext: return 0#paziņot man
	
	newTable = makeTable()
	
	pywikibot.output(newTable)
	
	if newTable!=currenttext:
		tableInserted = doreplace(lvtext,newTable,'<!-- TABLE START -->','<!-- TABLE END -->')
		
		thepage.text = tableInserted
		thepage.save(summary='Bots: atjaunināta tabula', botflag=True)
	else:
		print('no changes')
	
#
main()