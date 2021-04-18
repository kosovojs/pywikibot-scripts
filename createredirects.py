import pywikibot, os
from multiprocessing.dummy import Pool as ThreadPool

#os.chdir(r'projects/redirect')

REDIRECT = '#REDIRECT [[{}]]'

site = pywikibot.Site("lv", "wikipedia")

pairs= []

files = [
	#'lvwiki-visicilveki-redirects-tocrete.txt',
	'lvwiki-visicilveki-redirects-tocrete-2222.txt',
	'lvwiki-visicilveki-redirects-tocrete2.txt',
	'lvwiki-visicilveki-redirects-enwiki-uzv.txt'
]

for file in files:
	curfile = eval(open(file,'r', encoding='utf-8').read())
	pairs.extend(curfile)
print(len(pairs))

def one_r(id):
	redirectpage,target = id
	redpage = pywikibot.Page(site,redirectpage)
	
	if redpage.exists():
		return
	
	target = target[0]
	#redpage.put(REDIRECT.format(target), 'Pāradresē uz [[%s]]' % target)
	
	redpage.text = REDIRECT.format(target)
	redpage.save(summary='Pāradresē uz [[%s]]' % target, as_group='sysop')
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