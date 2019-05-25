import re, pywikibot, operator, os
from natsort import natsorted
from datetime import datetime

#os.chdir(r'projects/treisijs')

lvwiki = pywikibot.Site("lv", "wikipedia")

file = open("tresija saraksts-raw dsdfsdfsdf- fdfsfsdfsd v2-maina.txt", "w", encoding='utf-8')

wplist = set(['abwiki', 'acewiki', 'adywiki', 'afwiki', 'akwiki', 'amwiki', 'anwiki', 'angwiki', 'arwiki', 'arcwiki', 'arzwiki', 'aswiki', 'astwiki', 'atjwiki', 'avwiki', 'aywiki', 'azwiki', 'azbwiki', 'bawiki', 'barwiki', 'bclwiki', 'bewiki', 'be_x_oldwiki', 'bgwiki', 'bhwiki', 'biwiki', 'bjnwiki', 'bmwiki', 'bnwiki', 'bowiki', 'bpywiki', 'brwiki', 'bswiki', 'bugwiki', 'bxrwiki', 'cawiki', 'cbk_zamwiki', 'cdowiki', 'cewiki', 'cebwiki', 'chwiki', 'chrwiki', 'chywiki', 'ckbwiki', 'cowiki', 'crwiki', 'crhwiki', 'cswiki', 'csbwiki', 'cuwiki', 'cvwiki', 'cywiki', 'dawiki', 'dewiki', 'dinwiki', 'diqwiki', 'dsbwiki', 'dtywiki', 'dvwiki', 'dzwiki', 'eewiki', 'elwiki', 'emlwiki', 'test2wiki', 'enwiki', 'testwiki', 'simplewiki', 'eowiki', 'eswiki', 'etwiki', 'euwiki', 'extwiki', 'fawiki', 'ffwiki', 'fiwiki', 'fjwiki', 'fowiki', 'frwiki', 'frpwiki', 'frrwiki', 'furwiki', 'fywiki', 'gawiki', 'gagwiki', 'ganwiki', 'gdwiki', 'glwiki', 'glkwiki', 'gnwiki', 'gomwiki', 'gotwiki', 'alswiki', 'guwiki', 'gvwiki', 'hawiki', 'hakwiki', 'hawwiki', 'hewiki', 'hiwiki', 'hifwiki', 'hrwiki', 'hsbwiki', 'htwiki', 'huwiki', 'hywiki', 'iawiki', 'idwiki', 'iewiki', 'igwiki', 'ikwiki', 'ilowiki', 'iowiki', 'iswiki', 'itwiki', 'iuwiki', 'jawiki', 'jamwiki', 'jbowiki', 'jvwiki', 'kawiki', 'kaawiki', 'kabwiki', 'kbdwiki', 'kbpwiki', 'kgwiki', 'kiwiki', 'kkwiki', 'klwiki', 'kmwiki', 'knwiki', 'kowiki', 'koiwiki', 'krcwiki', 'kswiki', 'kshwiki', 'kuwiki', 'kvwiki', 'kwwiki', 'kywiki', 'lawiki', 'ladwiki', 'lbwiki', 'lbewiki', 'lezwiki', 'lgwiki', 'liwiki', 'lijwiki', 'lmowiki', 'lnwiki', 'lowiki', 'lrcwiki', 'ltwiki', 'ltgwiki', 'lvwiki', 'zh_classicalwiki', 'maiwiki', 'map_bmswiki', 'mdfwiki', 'mgwiki', 'mhrwiki', 'miwiki', 'minwiki', 'mkwiki', 'mlwiki', 'mnwiki', 'mrwiki', 'mrjwiki', 'mswiki', 'mtwiki', 'mwlwiki', 'mywiki', 'myvwiki', 'mznwiki', 'nawiki', 'nahwiki', 'zh_min_nanwiki', 'napwiki', 'nowiki', 'ndswiki', 'nds_nlwiki', 'newiki', 'newwiki', 'nlwiki', 'nnwiki', 'novwiki', 'nrmwiki', 'nsowiki', 'nvwiki', 'nywiki', 'ocwiki', 'olowiki', 'omwiki', 'orwiki', 'oswiki', 'pawiki', 'pagwiki', 'pamwiki', 'papwiki', 'pcdwiki', 'pdcwiki', 'pflwiki', 'piwiki', 'pihwiki', 'plwiki', 'pmswiki', 'pnbwiki', 'pntwiki', 'pswiki', 'ptwiki', 'quwiki', 'rmwiki', 'rmywiki', 'rnwiki', 'rowiki', 'roa_tarawiki', 'ruwiki', 'ruewiki', 'roa_rupwiki', 'rwwiki', 'sawiki', 'sahwiki', 'scwiki', 'scnwiki', 'scowiki', 'sdwiki', 'sewiki', 'sgwiki', 'bat_smgwiki', 'shwiki', 'siwiki', 'skwiki', 'slwiki', 'smwiki', 'snwiki', 'sowiki', 'sqwiki', 'srwiki', 'srnwiki', 'sswiki', 'stwiki', 'stqwiki', 'suwiki', 'svwiki', 'swwiki', 'szlwiki', 'tawiki', 'tcywiki', 'tewiki', 'tetwiki', 'tgwiki', 'thwiki', 'tiwiki', 'tkwiki', 'tlwiki', 'tnwiki', 'towiki', 'tpiwiki', 'trwiki', 'tswiki', 'ttwiki', 'tumwiki', 'twwiki', 'tywiki', 'tyvwiki', 'udmwiki', 'ugwiki', 'ukwiki', 'urwiki', 'uzwiki', 'vewiki', 'vecwiki', 'vepwiki', 'viwiki', 'vlswiki', 'vowiki', 'fiu_vrowiki', 'wawiki', 'warwiki', 'wowiki', 'wuuwiki', 'xalwiki', 'xhwiki', 'xmfwiki', 'yiwiki', 'yowiki', 'zh_yuewiki', 'zawiki', 'zeawiki', 'zhwiki', 'zuwiki'])

latvian = [
	('ā','a'),
	('ē','e'),
	('ī','i'),
	('ū','u'),
	('Ā','A'),
	('Ē','E'),
	('Ī','I'),
	('Ū','U'),
	##
	('Č','Cz'),
	('Ģ','Gz'),
	('Ķ','Kz'),
	('Ļ','Lz'),
	('Ņ','Nz'),
	('Š','Sz'),
	('Ž','Zz')
]

def multisub(subs, subject):
	"Simultaneously perform all substitutions on the subject string."
	pattern = '|'.join('(%s)' % re.escape(p) for p, s in subs)
	#pywikibot.output(pattern)
	substs = [s for p, s in subs]
	#pywikibot.output(substs)
	replace = lambda m: substs[m.lastindex - 1]
	#pywikibot.output(replace)
	return re.sub(pattern, replace, subject)
#

def fun(v):
	name = v[2]
	
	#for repl in latvian:
	#	name = name.replace(repl,latvian[repl])
	name = multisub(latvian, name)
	
	#pywikibot.output(name)
	return (-v[1],name)#

def getdata():
	lvpage = pywikibot.Page(lvwiki,"Vikipēdija:Raksti, kas nav latviešu valodas Vikipēdijā, bet ir visvairāk citu valodu Vikipēdijās")
	text = lvpage.get()
	
	itemlist = {}

	pattern = "\| ([^\n]+)\n\| ([^\n]+)\n\| ([^\n]+)\n\| ([^\n]+)\n"
	regex = re.compile(pattern)
	
	for match in regex.finditer(text):
		lvwikiarticle = match.group(1)
		secmat = match.group(2)
		itemregex = re.compile("\[\[:d:\s*([^\|]+)\|([^\]]+)\]\]")
		wditem = re.sub(itemregex,r'\1',secmat)
		enwiki = re.sub(itemregex,r'\2',secmat)
		
		itemlist.update({wditem:{'lv':lvwikiarticle,'en':enwiki}})
		
	#print('Found items: '+ str(len(itemlist)))
		
	return itemlist
	
filedata = eval(open('tresija saraksts_raw201704.txt','r', encoding='utf-8').read())

regexiw = "^...?wiki$"

otherwikis = ['be_x_oldwiki','cbk_zamwiki','simplewiki','nds_nlwiki','zh_min_nanwiki','map_bmswiki','zh_classicalwiki','zh_yuewiki','fiu_vrowiki','bat_smgwiki','roa_rupwiki','roa_tarawiki']

print(len(filedata))

fulldict = {}

for item in filedata:
	#thisdict = {}
	sites = filedata[item]
	
	#newlinks = [wiki for wiki in sites if re.match(regexiw,wiki) or wiki in otherwikis]
	
	iws = len(set(sites)&wplist)#len(newlinks)
	fulldict.update({item:iws})
#
cur_date = datetime.now().strftime("%Y-%m-%d")

jaunais = []

current = getdata()
for parsingarticle in fulldict:
	article = parsingarticle
	artdata = fulldict[article]
	originalwddata = filedata[parsingarticle]
	#ielikt enwiki un lvwiki nosaukumus no wd data
	lvwikiarticle = originalwddata['lvwiki'] if 'lvwiki' in originalwddata else ''
	enwikiarticle = originalwddata['enwiki'] if 'enwiki' in originalwddata else ''
	
	if article not in current:
		continue
	#jaunais.update({article:{'iws':artdata,'lv':current[article]['lv'],'en':current[article]['en']}})
	jaunais.append([article,artdata,current[article]['lv'],current[article]['en'],lvwikiarticle,enwikiarticle])
	
	
#

#jaunais = natsorted(jaunais, key=lambda x: #(-x[1],multisub(latvian, x[0])))
jaunais.sort(key=fun)

newlist = []

fdfdfsdfsdfsdfsdf = []
removed = []
for line in jaunais:
	#thhhhisdata = jaunais[line]
	lv = line[2]
	wd = line[0]
	en = line[3]
	iws = line[1]
	lvupd = line[4]
	enupd = line[5]
	
	if lvupd!='':
		newlist.append([lv,lvupd])
		removed.append(line)
		#lv = "[[{}]]".format(lvupd)
		if not re.search('^\d+\. gads$',lvupd):
			continue
	
	if enupd!='':
		en = enupd
	#
	if int(iws)<=51:
		removed.append(line)
		continue
		
	stringo = "| {}\n| [[:d:{}|{}]]\n| {}\n| {}\n|-".format(lv,wd,en,iws,cur_date)
	#file.write(stringo+'\n')
	fdfdfsdfsdfsdfsdf.append(stringo)
#########################################
pywikibot.output(removed)

info_header = '<!-- COUNT BEGIN -->'
info_footer = '<!-- COUNT END -->'

list_header = '<!-- LIST BEGIN -->'
list_footer = '<!-- LIST END -->'

def doreplace(text,pretext,header,footer):
	newtext = re.sub(header + '.*' + footer, header + pretext + footer, text, flags=re.DOTALL)
	#pywikibot.output(newtext)
	
	return newtext
#
def print_count(count):
	count = int(count)
	#if mm._mod(math.abs(number),10) == 1 and mm._mod(math.abs(number),100) ~= 11 then
	if (count % 10==1) and (count % 100!=11):
		return "{} raksts".format(count)
	else:
		return "{} raksti".format(count)
#
def get_wikilink(link):
	link323 = re.search('\[\[([^\]\|]+)',link)
	if link323:
		return link323.group(1)
	else:
		link
#
def generate_summary(articles):
	#re.search('^\d+\. gads$',lvupd)
	arts = [get_wikilink(f[2]) for f in articles if not re.search('^\d+\. gads$',f[4])]
	
	pywikibot.output(arts)
	
	comment = "-{} ({})".format(len(arts), ', '.join(arts))
	
	return comment
	
	
lvpage = pywikibot.Page(lvwiki,"Vikipēdija:Raksti, kas nav latviešu valodas Vikipēdijā, bet ir visvairāk citu valodu Vikipēdijās")
text = lvpage.get()
newtext = doreplace(text,'\n' + '\n'.join(fdfdfsdfsdfsdfsdf) + '\n',list_header,list_footer)
newtext = doreplace(newtext,print_count(str(len(fdfdfsdfsdfsdfsdf))),info_header,info_footer)

#lvpage2 = pywikibot.Page(lvwiki,"Dalībnieks:Edgars2007/Smilšu kaste")
lvpage.text = newtext
summarytext = generate_summary(removed)

makesection = True

#if len(summarytext)>250:
#	summarytext = 'bots: atjaunināts, detaļas [[Vikipēdijas diskusija:Raksti, kas nav latviešu valodas Vikipēdijā, bet ir visvairāk citu valodu Vikipēdijās|diskusiju lapā]]'
	#makesection = True

lvpage.save(summary=summarytext, botflag=False, minor=False)

###################make diskiusija:
#fix: 
#izņemtajiem sarakstiem - QS komandas
#pāradresācijām: re.findall() + reāli salīdzināt
diks1 = """=== Pāradresācijas ===
Izveidotie raksti, kam nosaukums nesakrīt ar sarakstā esošo:
{}
"""

diks2 = """=== Izņemtie raksti ===
No saraksta izņemtie raksti:
{}
"""
#newlist
fsdfdf = []
for pair in newlist:
	red,art = pair

	red = red.replace('<','&lt;').replace('>','&gt;')
	fsdfdf.append("* [[{}]] - {}".format(art,red))
#
diks1 = diks1.format('\n'.join(fsdfdf))

if makesection:
	sect = []
	for recrom in removed:
		sect.append("| {}\n| [[:d:{}|{}]]\n| {}\n|-".format(recrom[2],recrom[0],recrom[5],recrom[1]))
#
dfsdf = """{{| class="sortable wikitable"
|-
! width="320" | Vajadzīgais raksts
! width="320" | Saite uz Vikidatiem (nosaukums angļu valodā)
! "Starpviki"<br />skaits
|-
{}
|}}""".format('\n'.join(sect))
diks2 = diks2.format(dfsdf)


tosaveindisc = "== Atjaunināšana ==\n{}\n\n{}".format(diks1,diks2)

lvpage3 = pywikibot.Page(lvwiki,"Vikipēdijas diskusija:Raksti, kas nav latviešu valodas Vikipēdijā, bet ir visvairāk citu valodu Vikipēdijās")
text3 = lvpage3.get()
newtext3 = doreplace(text3,'\n' + tosaveindisc + '\n','<!-- REDIRECTS START -->','<!-- REDIRECTS END -->')

lvpage3.text = newtext3
#lvpage3.save(summary='atjaunināts')
############################################
file2 = open("tresija saraksts-redirects.txt", "w", encoding='utf-8')
file2.write(str(newlist))
"""
for line in jaunais:
	thhhhisdata = jaunais[line]
	lv = thhhhisdata['lv']
	wd = thhhhisdata['wd']
	en = thhhhisdata['en']
	iws = thhhhisdata['iws']
	
	stringo = "| {}\n| [[:d:{}|{}]]\n| {}\n| 2017-03-04\n|-".format(lv,wd,en,iws)
	file.write(stringo+'\n')
"""