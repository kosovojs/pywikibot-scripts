import pywikibot, re, calendar

sagatave = "Veidne:Vai tu zināji/Sagatave"#"Dalībnieks:Edgars2007/Dyk sagatave"
sagatave2 = "Veidne:Vai tu zināji/Sagatave"
ieteikumi = "Veidne:Vai tu zināji/Ieteiktie fakti"
import datetime
from datetime import date, timedelta
yesterday = date.today() + timedelta(1)
lastday =  yesterday.strftime('%d')

currDate = datetime.datetime.now()
daysInMonth = datetime.datetime.now()

dienas =1
sakums = int(lastday)
daysmonth = calendar.monthrange(currDate.year, currDate.month)[1]

summarytext = "Bots: faktu pievienošana Sākumlapai"

#file = open("dz-vieta-hokejisti.txt", "w", encoding='utf-8')

site = pywikibot.Site("lv", "wikipedia", user='Edgars2007')

def formatImage(group1, group2, group3):
	group3 = group3 or ''
	group2 = group2 or ''
	group1 = group1 or ''
	
	if group3!='':
		string = "{{#ifeq:{{{2|}}}|att|{{space}}"+group2+"}}"+group3
	else:
		string = group1+"{{#ifeq:{{{2|}}}|att|"+group2+"}}"
		
	return string

def getFacts(text,end):
	splittedtext = text.split('\n<!--dyk diena -->\n')
	
	splittedtext = splittedtext[1:end]
	
	splittedtextRET = '\n<!--dyk diena -->\n'.join(splittedtext)
	
	splittedtextRET = '<!--dyk diena -->\n'+splittedtextRET
	
	usedfacts = splittedtext[::-1]
	
	used = '\n\n'.join(usedfacts)
	
	return splittedtext,used,splittedtextRET
	
def cleanPage(text,usedFacts,splittedtextRET):
	archivetext = "{{ombox | text = Saraksta sākumā ir jaunākie fakti}}"
	
	usedFacts = re.sub(r'(\[\[Attēls:.*\|)(\d+px)\]\]', r'\g<1>50px]]',usedFacts)
	
	newarchive = archivetext+"\n\n"+usedFacts
	
	text = text.replace(splittedtextRET,'')
	text = text.replace(archivetext,newarchive)
	
	return text
	
def addFacts(text,comment):
	oldtext = "}}<noinclude>\n{{dokumentācija|Veidne:Vai tu zināji/doc}}</noinclude>"
	newtext = str(comment)+"\n}}<noinclude>\n{{dokumentācija|Veidne:Vai tu zināji/doc}}</noinclude>"
	
	text = text.replace(oldtext,newtext)
	
	return text
	
def addFactsF(facts):
	#pywikibot.output(facts)
	
	nextDay = sakums
	
	factjoiner = []
	
	counter = 0
	
	for day in facts:
		#pywikibot.output(day)
		
	#"""
		#if counter<days:
		if nextDay==daysmonth:
			switcher = str(nextDay)+'|0'
			comment = nextDay
			nextDay = 1
		else:
			switcher = nextDay
			comment = nextDay
			nextDay += 1
				
		#dfsdf = day[counter]
		counter +=1
		
		searchres = re.search('(\[\[Attēls:.*\|\d+px\]\])\n([^$]+)',day)
		
		if searchres:
			file = searchres.group(1)
			dayfacts = searchres.group(2)
			
			dayfactsFILE = re.search('(.)(<small>.+?<\/small>)([\.\?\!\,\:])?',dayfacts)
			
			if dayfactsFILE:
				gr1 = dayfactsFILE.group(1) or ''
				gr2 = dayfactsFILE.group(2) or ''
				gr3 = dayfactsFILE.group(3) or ''
				
				imageformatterOLD = gr1+gr2+gr3
				imageformatter = formatImage(gr1, gr2, gr3)
				
				dayfacts = dayfacts.replace(imageformatterOLD,imageformatter)
			
		#formatfile
			
				tojoiner = "<!--"+str(comment)+". datums\n-->|"+str(switcher)+"={{#ifeq:{{{2|}}}|att|"+str(file)+"}}\n"+str(dayfacts)
				factjoiner.append(tojoiner)
			
			
	joinedFacts = '\n'.join(factjoiner)
	#pywikibot.output(joinedFacts)
	
	return joinedFacts
	#"""
	
def main():
	saglapa = pywikibot.Page(site,sagatave)
	saglapaFROMcopy = pywikibot.Page(site,sagatave2)
	ietlapa = pywikibot.Page(site,ieteikumi)
	
	sagatT = saglapaFROMcopy.get()
	ieteikumuText = ietlapa.get()
	#pywikibot.output(ieteikumuText)
	sagataveText = saglapa.get()
	
	splittedtext,used,splittedtextRET = getFacts(ieteikumuText,dienas+1)
	
	factstoadd = addFactsF(splittedtext)
	
	if '... ...' in  factstoadd or '[[Attēls:...|' in factstoadd: return 0
	
	sagataveNEW = addFacts(sagatT,factstoadd)
	
	saglapa.text = sagataveNEW
	
	ieteikumiNEW = cleanPage(ieteikumuText,used,splittedtextRET)
	
	ietlapa.text = ieteikumiNEW
	
	#pywikibot.showDiff(ieteikumuText, ieteikumiNEW)
	#pywikibot.showDiff(sagataveText, sagataveNEW)
	
	saglapa.save(summary=summarytext, botflag=False, minor=False)
	ietlapa.save(summary=summarytext, botflag=False, minor=False)
	
	return 1
	
#if __name__ == "__main__":
#	main()