import pywikibot, re, mwparserfromhell
from datetime import datetime

templateCheck = "#invoke:sports table"
enwp = pywikibot.Site("en", "wikipedia")
lvwp = pywikibot.Site("lv", "wikipedia")

currenttime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

true = True
false = False
configuration = pywikibot.Page(lvwp,'Dalībnieks:Edgars2007/Hokejs.json')
configuration = configuration.get()
configuration = eval(configuration)

lvwikipage = configuration['lv'][0]
enwikipage = configuration['en'][0]

botflag = configuration['botflag'] if 'botflag' in configuration else True

removeparams = configuration['remove']#note_res_KE varbūt arī nevajag ņemt ārā

def makeupdate(date):
	
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
	#
	
	for article in mapper:
		#pywikibot.output("Working on %s" % article)
		enwikitable = mapper[article]
		lvtemplate = mapper_lv_tpl[article]
		
		returnedtext = groupchange(enwikitable,lvtemplate)
		returning.update({article:returnedtext})
		
		#text = text.replace(lvwikitable,'\n\n'+returnedtext+'\n\n')
		
		#page.text = text
		
		#page.save(comment='Bots: atjaunināta tabula', botflag=True, minor=False)
		
	return returning#{'a':a,'b':b}

def groupchange(enarticle,lvtemplate):
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
			#
			
			tpl.add('template_name',lvtemplate)
			
			newtext = str(tpl)
			
			
			#newtext = newtext.replace('] and [','] un [')
			#
		
			for replace in configuration["repls"]:
				thisrepl = configuration["repls"][replace]
				newtext = newtext.replace(replace,thisrepl)
		
	#
	
	lvpage = pywikibot.Page(lvwp,'Veidne:'+lvtemplate)
	lvtext = lvpage.get()
	lvtextOLD = lvtext
	newtext += '<noinclude>\n[[Kategorija:Vikipēdijas veidnes]]</noinclude>'
	
	if newtext!=lvtextOLD:
		
		lvpage.text = newtext
		lvpage.save(summary='bots: atjaunināts', botflag=botflag, minor=False)
	else:
		pywikibot.output('No changes to {}'.format(lvtemplate))
		
	
	return newtext

mapper = {
	'A':configuration['en'][1],
	'B':configuration['en'][2]
}

mapper_lv_tpl = {
	"A":configuration['lv'][1],
	"B":configuration['lv'][2]
}
linkpatt = "\[\[[^\|]+\|(\d+)[–-](\d+)([^\]]*?)\]\]"#"\[\[[^\|]+\|([^\]]+)\]\]"
linkpatt2 = "\[\[[^\|]+\|([^\]]+)\]\]"
daypatt = "(\d+) May 2018"

def getgames(text):
	text = text.partition('{| style="width:100%;" cellspacing="1"')
	mytext = str.strip(text[1] + text[2])
	
	mytext = re.sub(linkpatt,r'\1:\2\3',mytext)
	mytext = re.sub(linkpatt2,r'',mytext)
	
	mytext = re.sub(daypatt,r'\1. maijs',mytext)
	
	mytext = mytext.replace('GWS)','{{piezīme|GWS|Uzvara gūta pēcspēles metienu sērijā}})')
	mytext = mytext.replace('OT)','{{piezīme|OT|Uzvara gūta spēles pagarinājumā}})')
	
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
	print(currenttime)
	if configuration["STOP"]:
		print('Config has STOP=true')
		return 0
	
	mmmm = {}
	endata = getsections()#eval(open('hokeja tests.txt', 'r', encoding='utf-8').read())#getsections()
	mmmm.update({'AG':getgames(endata['aG'])})
	mmmm.update({'BG':getgames(endata['bG'])})
	mmmm.update({'AT':endata['A']})
	mmmm.update({'BT':endata['B']})
	
	lvpage = pywikibot.Page(lvwp,lvwikipage)
	lvtext = lvpage.get()
	lvtextOLD = lvtext
	
	for gfdgf in mmmm:
		lvtext = doreplace(lvtext,mmmm[gfdgf],'<!-- {} BEGIN -->'.format(gfdgf),'<!-- {} END -->'.format(gfdgf))
	
	#fileS = open('hokeja tests.txt', 'w', encoding='utf-8')
	#fileS.write(str(endata))
	
	for replace in configuration["repls"]:
		thisrepl = configuration["repls"][replace]
		lvtext = lvtext.replace(replace,thisrepl)
		
	#fileS = open('hokeja tests2.txt', 'w', encoding='utf-8')
	#fileS.write(str(lvtext))
	
	if lvtext!=lvtextOLD:
		lvpage.text = lvtext
		lvpage.save(summary='bots: atjaunināts', botflag=botflag, minor=False)
	else:
		print('No changes to main article')
#

if __name__ == "__main__":
	main()