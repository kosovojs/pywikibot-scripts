import pywikibot, os
#from multiprocessing.dummy import Pool as ThreadPool

#os.chdir(r'projects/redirect')

REDIRECT = '#REDIRECT [[{}]]'

site = pywikibot.Site("lv", "wikipedia")

pairs = eval(open('lvwiki-visicilveki-redirects-enwiki-uzv.txt','r', encoding='utf-8').read())
print(len(pairs))

def one_r(id):
	redirectpage,target = id
	redpage = pywikibot.Page(site,redirectpage)
	
	if redpage.exists():
		return
	
	target = target[0]
	#redpage.put(REDIRECT.format(target), 'Pāradresē uz [[%s]]' % target)
	
	redpage.text = REDIRECT.format(target)
	redpage.save(summary='bots: pāradresācija uz [[%s]] (job002)' % target, as_group='sysop')
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