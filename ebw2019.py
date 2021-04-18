import pywikibot, re, mwparserfromhell

templateCheck = "#invoke:sports table"
removeparams= ["template_name","update","start_date","class_rules","note_SAS","note_PES","hth_RUS","hth_LAT",'hth_ESP','hth_HUN','hth_SVN','hth_GRE']#note_res_KE varbūt arī nevajag ņemt ārā

enwp = pywikibot.Site("en", "wikipedia")
lvwp = pywikibot.Site("lv", "wikipedia")

lvwikipage = '2019. gada Eiropas čempionāts basketbolā sievietēm'
enwikipage = 'FIBA Women\'s EuroBasket 2019'

def makeupdate(date):
	from datetime import datetime
	mon = {
		'1':'janvāris',
		'2':'februāris',
		'3':'marts',
		'4':'aprīlis',
		'5':'maijs',
		'6':'jūnijs',
		'7':'jūlijs',
		'8':'augusts',
		'9':'septembris',
		'10':'oktobris',
		'11':'novembris',
		'12':'decembris'
	}
	f = "%-d %B %Y"
	datetime = datetime.strptime(date, f)
	#print(datetime.timetuple())
	#http://stackoverflow.com/questions/17118071/python-add-leading-zeroes-using-str-format
	
	dateee = "{}. gada {}. {}".format(datetime.year,datetime.day,mon[str(datetime.month)])
	
	return dateee
#
def getsections():
	enpage = pywikibot.Page(enwp,enwikipage)
	entext = enpage.get()
	wikicode = mwparserfromhell.parse(entext)
	sections = wikicode.get_sections(include_lead=False,include_headings=True)
	
	returning = {}
	
	for section in sections:
		header = section.get(0)
		title = str.strip(str(header.title))#.lower()
		if title == "Group A":
			section.remove(header)
			a = str(section)
			returning.update({'aG':a})
		elif title == "Group B":
			section.remove(header)
			b = str(section)
			returning.update({'bG':b})
		elif title == "Group C":
			section.remove(header)
			c = str(section)
			returning.update({'cG':c})
		elif title == "Group D":
			section.remove(header)
			d = str(section)
			returning.update({'dG':d})
	#
	
	for article in mapper:
		#pywikibot.output("Working on %s" % article)
		enwikitable = mapper[article]
		
		returnedtext = groupchange(enwikitable)
		returning.update({article:returnedtext})
		
		#text = text.replace(lvwikitable,'\n\n'+returnedtext+'\n\n')
		
		#page.text = text
		
		#page.save(comment='Bots: atjaunināta tabula', botflag=True, minor=False)
		
	return returning#{'a':a,'b':b}

def groupchange(enarticle):
	#enarticle = "Template:2016–17 Premier League table"
	enpage = pywikibot.Page(enwp,enarticle)
	entext = enpage.get()
	enwikicode = mwparserfromhell.parse(entext)
	templates = enwikicode.filter_templates()
	

	for tpl in templates:
		if tpl.name.lower().strip() in templateCheck:
			#pywikibot.output(tpl)
		
			for param in removeparams:
				if tpl.has(param):
					tpl.remove(param)
				
			newtext = str(tpl)
			
			
			#newtext = newtext.replace('] and [','] un [')
			#
		
			newtext = newtext.replace(r'[[EuroBasket Women 2019 final round|Quarterfinals]]',
									  r'Ceturtdaļfināls')
			newtext = newtext.replace(r'[[EuroBasket Women 2019 final round|Qualification for quarterfinals]]',
									  r'Astotdaļfināls')
									  
	return newtext

mapper = {
	"A":"EuroBasket Women 2019 Group A",
	"B":"EuroBasket Women 2019 Group B",
	"C":"EuroBasket Women 2019 Group C",
	"D":"EuroBasket Women 2019 Group D",
}

linkpatt = "\[\[[^\|]+\|(\d+)[–-](\d+)([^\]]*?)\]\]"#"\[\[[^\|]+\|([^\]]+)\]\]"
linkpatt2 = "\[\[[^\|]+\|([^\]]+)\]\]"
daypatt = "(\d+) June 2019"
daypatt2 = "(\d+) July 2019"

def getgames(text):
	text = text.partition('{| style="width:100%;" cellspacing="1"')
	mytext = str.strip(text[1] + text[2])
	
	mytext = mytext.replace('([[Overtime (sports)#Basketball|OT]])','({{piezīme|OT|Uzvara gūta spēles pagarinājumā}})')
	
	mytext = re.sub(linkpatt,r'\1:\2\3',mytext)
	mytext = re.sub(linkpatt2,r'',mytext)
	
	mytext = re.sub(daypatt,r'\1. jūnijs',mytext)
	mytext = re.sub(daypatt2,r'\1. jūlijs',mytext)
	
	mytext = mytext.replace('GWS)','{{piezīme|GWS|Uzvara gūta pēcspēles metienu sērijā}})')
	
	mytext = mytext.replace('align=center|','style="text-align:center; font-weight:bold;" | ')
	mytext = mytext.replace(' style=font-size:90%',' style="font-size:95%;"')
	
	return mytext
	#pywikibot.output(mytext)
	
def doreplace(text,pretext,header,footer):
	newtext = re.sub(header + '.*' + footer, header + '\n' + pretext + '\n' + footer, text, flags=re.DOTALL)
	#pywikibot.output(newtext)
	
	return newtext
#
def main():
	mmmm = {}
	endata = getsections()#eval(open('hokeja tests.txt', 'r', encoding='utf-8').read())#getsections()
	mmmm.update({'AG':getgames(endata['aG'])})
	mmmm.update({'BG':getgames(endata['bG'])})
	mmmm.update({'CG':getgames(endata['cG'])})
	mmmm.update({'DG':getgames(endata['dG'])})
	mmmm.update({'AT':endata['A']})
	mmmm.update({'BT':endata['B']})
	mmmm.update({'CT':endata['C']})
	mmmm.update({'DT':endata['D']})
	
	lvpage = pywikibot.Page(lvwp,lvwikipage)
	lvtext = lvpage.get()
	lvtextOLD = lvtext
	
	for gfdgf in mmmm:
		lvtext = doreplace(lvtext,mmmm[gfdgf],'<!-- {} BEGIN -->'.format(gfdgf),'<!-- {} END -->'.format(gfdgf))
	
	#fileS = open('hokeja tests.txt', 'w', encoding='utf-8')
	#fileS.write(str(endata))
	
	lvtext = lvtext.replace(r'[[EuroBasket Women 2019 final round|Quarterfinals]]',
									  r'Ceturtdaļfināls')
	lvtext = lvtext.replace(r'[[EuroBasket Women 2019 final round|Qualification for quarterfinals]]',
									  r'Astotdaļfināls')
									  
									  
	#fileS = open('hokeja tests2.txt', 'w', encoding='utf-8')
	#fileS.write(str(lvtext))
	
	if lvtext!=lvtextOLD:
	
		lvpage.put(lvtext, "Bots: atjaunināts")
	else:
		print('No changes')
#

if __name__ == "__main__":
	main()