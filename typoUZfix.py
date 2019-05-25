import re, pywikibot, datetime, time, os
from pywikibot import xmlreader
from pywikibot import textlib

site = pywikibot.Site("uz", "wikipedia")

#os.chdir(r'projects/uzwiki')

vers = '0.5'

thelist = eval(open('uzwiki-check-typo.txt','r', encoding='utf-8').read())

'''
a - atseviski
s - tikai, ja vārda sākumā
c - capital
l - lowercase all
'''
regs = [
	['([Yy])anv\.(?!\s*(da|ning))',r'\1anvar',['s']],
	['([Yy])anv\.\s*(da|ning)',r'\1anvar\2',['s']],
	['([Ff])ev\.(?!\s*(da|ning))',r'\1evral',['s']],
	['([Ff])ev\.\s*(da|ning)',r'\1evral\2',['s']],
	['([Aa])pr\.(?!\s*(da|ning))',r'\1prel',['s']],
	['([Aa])pr\.\s*(da|ning)',r'\1prel\2',['s']],
	['([Aa])vg\s*\.(?!\s*(da|ning))',r'\1vgust',['s']],
	['([Aa])vg\.\s*(da|ning)',r'\1vgust\2',['s']],
	['([Ss])ent\.(?!\s*(da|ning))',r'\1entabr',['s']],
	['([Ss])ent\.\s*(da|ning)',r'\1entabr\2',['s']],
	['([Oo])kt\.(?!\s*(da|ning))',r'\1ktabr',['s']],
	['([Oo])kt\.\s*(da|ning)',r'\1ktabr\2',['s']],
	['([Nn])oyab\.(?!\s*(da|ning))',r'\1oyabr',['s']],
	['([Nn])oyab\.\s*(da|ning)',r'\1oyabr\2',['s']],
	['([Dd])ek\.(?!\s*(da|ning))',r'\1ekabr',['s']],
	['([Dd])ek\.\s*(da|ning)',r'\1ekabr\2',['s']],
	['(\d+)-?a\.lar',r'\1-asrlar'],
	['(\d+)-?a\.(ni(ng)?)',r'\1-asr\2'],
	['(\d+)-?a\.',r'\1-asr'],
	['b-n','bilan',['a']],#tikai, ja atsevišķi
	#['va b\.','va boshqalar'],
	['at\.\s*m\.','atom massasi',['s']],
	['d-?r','doktor',['s']],
	['([Bb])al\.',r'\1alandligi',['s']],
	['f-?ka?','fabrika',['s']],#begin
	['f-t','fakultet',['s']],
	['va h\.\s*k\.','va hokazo.',['s']],
	['([Hh])oz\.',r'\1ozirgi',['s']],
	['FA','fanlar akademiyasi',['a','c']],
	#['i\.\s*ch\.','ishlab chiqarish'],
	['([Ii])n-?t',r'\1nstitut',['s']],
	['([Uu])n-?t',r'\1niversitet',['s']],
	#['i\.\s*t\.','ilmiy tadqiqot',['s','l']],
	['k-z','kolxoz',['s']],
	['s-z','sovxoz',['s']],
	['kVt-soat','Kilovatt-soat'],
	['k-t','kombinat',['s']],
	['([Ll])ab\.',r'\1aboratoriya',['s']],
	['([Mm])ayd\.',r'\1aydon'],
	['([Pp])rof\.',r'\1rofessor',['s']],
	['([Qq])ad\.',r'\1adimgi'],
	['q\.\s*x\.','qishloq xoʻjaligi'],
	['k-?t','kombinat',['s']],
	['r-n','rayon',['s']],
	['([Rr])ej\.',r'\1ejissyor',['s']],
	['RF','Rossiya Federatsiyasi',['a','c']],
	['RF\s*dagi','Rossiya Federatsiyasidagi',['a','c']],
	#Toshkent Davlat Universitet - jāieliek
	['([Rr])adiost-ya',r'\1adiostansiya'],
	['([Tt])elest-ya',r'\1elestansiya'],
	['([Ss])t-ya',r'\1tansiya',['s']],
	#['([Ss])h\.',r'\1hahri',['a']],
	#['([Ss])h\.lar',r'\1haharlar'],
	['([Tt])axm\.',r'\1axminan'],
	['([Tt])-?ra(si|da|gacha|lar|lari)',r'\1emperatura\2',['a']],
	['([Tt])\.\s*y\.',r'\1emir yoʻl',['s']],
	['([Uu])n-?t',r'\1niversitet',['s']],
	#['y.lar','yillar'], - raksta nosaukums - sākās :(
	#['([Yy])a\.\s*o\.',r'\1arim orol',['s']],
	#['`','ʻ'],#no tpls, etc.
	['z-?d','zavod',['s']],
	['1-?jahon urushi','Birinchi jahon urushi'],
	['2-?jahon urushi','Ikkinchi jahon urushi'],
	['OʻzR','Oʻzbekiston Respublikasi',['s']],
	['\(q\.','(qarang',['s']],
	['([Jj])an\.',r'\1anubiy',['s']],
	['Axolisi','Aholisi',['c']],
	['([Jj])an\.-sharqida',r'\1anubi-sharqida'],
	['([Ss])him\.-sharqida',r'\1himoli-sharqida'],
	['([Jj])an\.gʻarbida',r'\1anubi-gʻarbida'],
	['([Ss])him\.gʻarbida',r'\1himoli-gʻarbida'],
	['([Jj])an\.dagi',r'\1anubidagi'],
	['([Ss])him\.dagi',r'\1himolidagi'],
	['([Jj])an\.da',r'\1anubida'],
	['([Ss])him\.da',r'\1himolida'],
	['([Jj])an\.dan',r'\1anubidan'],
	['([Ss])him\.dan',r'\1himolidan'],
	['Hitoy','Xitoy',['c']]
]

'''
a - atseviski
s - tikai, ja vārda sākumā
c - capital
l - lowercase all
'''

regssearch = []

def regexes(one):
	#return
	
	if len(one)==2:
		return re.compile('(?![A-Za-zʻ])'+one[0])
	else:
		currflags = None
		searchstr = one[0]
		flags = one[2]
		if 'a' in flags:
			searchstr = '(?![A-Za-zʻ])'+searchstr+'(?![A-Za-zʻ])'
		if 's' in flags:
			searchstr = '(?![A-Za-zʻ])'+searchstr
		if 'c' not in flags and 'l' not in flags:
			currflags = re.IGNORECASE
		
		if currflags:
			return re.compile(searchstr,currflags)
		else:
			return re.compile(searchstr)
#

def create_search_regexes():
	for one in regs:
		
		if len(one)==2:
			regssearch.append(re.compile(one[0],re.IGNORECASE))
		else:
			currflags = None
			searchstr = one[0]
			flags = one[2]
			if 'a' in flags:
				searchstr = '\b'+searchstr+'\b'
			if 's' in flags:
				searchstr = '\b'+searchstr
			if 'c' not in flags and 'l' not in flags:
				currflags = re.IGNORECASE
			
			if currflags:
				regssearch.append([re.compile(searchstr,currflags),one[1]])
			else:
				regssearch.append([re.compile(searchstr),one[1]])
#
def can_edit():
	page = pywikibot.Page(site,"Foydalanuvchi:EdgarsBot/STOP")
	pgtext = page.text
	
	if pgtext.strip()!='':
		return False
	else:
		return True
#

def edit_one_article(title):
	pywikibot.output(title)
	page = pywikibot.Page(site,title)
	pgtext = page.text
	oldtext = pgtext
	
	#if "NO BOTS" in pgtext: return 0
	
	for entry in regs:
		pgtext = re.sub(regexes(entry),entry[1],pgtext)
	
	if oldtext != pgtext:
		#pywikibot.showDiff(oldtext,pgtext)
		page.text = pgtext
		page.save(summary='qisqartmalarni toʻliqlash (p1, v{})'.format(vers), botflag=True, minor=False)
#
def main():
	ind = 0
	
	#thelist = ['Bon Jovi']
	for article in thelist:
		if (ind % 10)==0:
			if not can_edit():
				break
		ind += 1
		edit_one_article(article)
#
main()