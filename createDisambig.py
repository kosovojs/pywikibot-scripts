import pywikibot, os
from multiprocessing.dummy import Pool as ThreadPool

#os.chdir(r'projects/redirect')

site = pywikibot.Site("lv", "wikipedia")

pairs= []

bad = ['Terēze',
'Jr.',
'Jaunākais',
'jaunākais',
'Vilhelms',
'Eleonora',
'Kampenhauzens',
'Margarita',
'Vecais',
'Monika',
'Karolīne',
'Luīze']

files = [
	'cilveki-DISAMBIG-create (2).txt'
]

for file in files:
	curfile = eval(open(file,'r', encoding='utf-8').read())
	pairs.extend(curfile)
print(len(pairs))

def one_r(id):
	redirectpage,target = id
	if redirectpage in bad: return 0
	
	redpage = pywikibot.Page(site,redirectpage)
	
	if redpage.exists():
		return
	
	separ = ']];\n* [['
	page_text = "'''{}''' var būt:\n* [[{}]].\n\n{{{{uzvārds}}}}\n\n[[Kategorija:Uzvārdi]]".format(redirectpage,separ.join(target))
	#redpage.put(REDIRECT.format(target), 'Pāradresē uz [[%s]]' % target)
	
	redpage.text = page_text#REDIRECT.format(target)
	redpage.save(summary='jauna nozīmju atdalīšanas lapa: [[{}]]'.format(redirectpage), as_group='sysop')
#

pooling = False

if pooling:
	pool = ThreadPool(8)
	pool.map(one_r,pairs)
	pool.close()
	pool.join()
else:
	for one in pairs:
		one_r(one)