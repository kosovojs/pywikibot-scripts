import re, pywikibot, datetime, time, bz2, sys
from pywikibot import xmlreader
from pywikibot import textlib
from bz2 import BZ2File


xmlversion = '20180720'

#http://stackoverflow.com/questions/500864/case-insensitive-python-regular-expression-without-re-compile

print(datetime.datetime.now())

xmlfile = '{lang}wiki-{ver}-pages-articles.xml'.format(lang='uz',ver=xmlversion)
file_to_save = '{lang} - typolist [{ver}].txt'.format(lang='uz',ver=xmlversion)

file = open(file_to_save, "w", encoding='utf-8')

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
regs2 = [
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
	['(\d+)-?a\.',r'\1-asr'],
	['(\d+)-?a\.lar',r'\1-asrlar'],
	['(\d+)-?a\.ning',r'\1-asrning'],
	['b-n','bilan',['a']],#tikai, ja atsevišķi
	#['va b\.','va boshqalar'],
	['d-r','doktor',['s']],
	['f-k','fabrika',['s']],#begin
	['f-t','fakultet',['s']],
	['hoz\.','hozirgi',['s']],
	['FA','fanlar akademiyasi',['a','c']],
	['i\.ch\.','ishlab chiqarish'],
	['in-t','institut',['s']],
	['i\.\s*t\.','ilmiy tadqiqot',['s','l']],
	['k-z','kolxoz',['s']],
	['kVt-soat','Kilovatt-soat'],
	['k-t','kombinat',['s']],
	['([Ll])ab\.',r'\1aboratoriya',['s']],
	['([Mm])ayd\.',r'\1aydon'],
	['([Pp])rof\.',r'\1rofessor',['s']],
	['([Qq])ad\.',r'\1adimgi'],
	['q\.\s*x\.','qishloq xoʻjaligi'],
	['r-n','rayon',['s']],
	['([Rr])ej\.',r'\1ejissyor',['s']],
	['RF','Rossiya Federatsiyasi',['a','c']],
	['([Rr])adiost-ya',r'\1adiostansiya'],
	['([Tt])elest-ya',r'\1elestansiya'],
	['([Ss])h\.',r'\1hahri',['a']],
	['([Ss])h\.lar',r'\1haharlar'],
	['s-z','sovxoz',['s']],
	['([Tt])axm\.',r'\1axminan'],
	['([Tt])-ra',r'\1emperatura',['s']],
	['([Tt])\.y\.',r'\1emir yoʻl',['s']],
	['([Uu])n-?t',r'\1niversitet',['s']],
	#['y.lar','yillar'], - raksta nosaukums - sākās :(
	#['([Yy])a\.\s*o\.',r'\1arim orol',['s']],
	#['`','ʻ'],#no tpls, etc.
	['z-d','zavod',['s']],
	['1-?jahon urushi','Birinchi jahon urushi'],
	['2-?jahon urushi','Ikkinchi jahon urushi'],
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
regssearch = []

def create_search_regexes():
	for one in regs:
		
		if len(one)==2:
			regssearch.append(re.compile('(?![A-Za-zʻ])'+one[0],re.IGNORECASE))
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
				regssearch.append(re.compile(searchstr,currflags))
			else:
				regssearch.append(re.compile(searchstr))
#
create_search_regexes()


num = 0

context = 30

numprint = 75

finds = []

start = time.time()

#f = bz2.open('/mnt/nfs/dumps-labstore1006.wikimedia.org/xmldatadumps/public/lvwiki/20180620/lvwiki-20180620-pages-articles.xml.bz2', 'r')
'''
with bz2.BZ2File('/mnt/nfs/dumps-labstore1006.wikimedia.org/xmldatadumps/public/lvwiki/20180620/lvwiki-20180620-pages-articles.xml.bz2') as xml_file:
	for page in xmlreader.XmlDump(xml_file).parse():
		if page.ns == "0" and not page.isredirect:
			pagetext = textlib.unescape(page.text)
			pagetitle = page.title
			
			if num==1000:
				break
			
			num += 1
			if num % numprint == 0:
				print(num)
			
			for checkR in checklist:
				m = checkR.finditer(pagetext)
				if m:
					for found in m:
						sectionname = '<nowiki>'+pagetext[max(0, found.start() - context):found.start()]+'</nowiki><span style="background-color:#fdd;padding:2px;margin:1px">\'\'\''+pagetext[found.start():found.end()]+'\'\'\'</span><nowiki>'+pagetext[found.end() : found.end() + context] + '</nowiki>'
						sectionname = sectionname.replace('\n',' ')
						sectionname = re.sub('\s\s*',' ',sectionname)
						
						finds.append([pagetitle,checkR,sectionname])
					
file.write(str(finds))
end = time.time()
print('Took {} seconds to complete'.format(end-start))
'''

num = 0

context = 30

numprint = 2000

finds = []

start = time.time()

paths = '/public/dumps/public/uzwiki/20180720/uzwiki-20180720-pages-articles.xml.bz2'

with BZ2File(paths) as xml_file:
	blah = False
	for page in xmlreader.XmlDump(paths).parse():
		if page.ns == "0" and not page.isredirect:
			pagetext = textlib.unescape(page.text)
			pagetitle = page.title
            
			#if num==20000:
			#	break
			
			num += 1
			if num % numprint == 0:
				print(num)
				sys.stdout.flush()
		
			for checkR in regssearch:
				m = checkR.finditer(pagetext)
				if m:
					for found in m:
						sectionname = [pagetext[max(0, found.start() - context):found.start()],
						pagetext[found.start():found.end()],
						pagetext[found.end() : found.end() + context]
                        ]#'<nowiki>'+pagetext[max(0, found.start() - context):found.start()]+'</nowiki><span style="background-color:#fdd;padding:2px;margin:1px">\'\'\''+pagetext[found.start():found.end()]+'\'\'\'</span><nowiki>'+pagetext[found.end() : found.end() + context] + '</nowiki>'
						#sectionname = sectionname.replace('\n',' ')
                        
						#sectionname = re.sub('\s\s*',' ',sectionname)
						blah = True
						finds.append([pagetitle,checkR,sectionname])
					
file.write(str(finds))
end = time.time()
print('Took {} seconds to complete'.format(end-start))
file.close()