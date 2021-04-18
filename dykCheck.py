import pywikibot, datetime

site = pywikibot.Site("lv", "wikipedia")
site.login()
site.get_tokens('edit')

def doAPI(datestr):
	r = pywikibot.data.api.Request(site=site, action="expandtemplates", format="json", 
									text='{{Vai tu zināji/Sagatave|' + datestr + '}}', prop='wikitext').submit()
	#
	outputstr = r['expandtemplates']['wikitext']
	return outputstr
#

message = """{{ping|Biafra|Edgars2007|Papuass|ScAvenger}} lapā "[[Veidne:Vai tu zināji/Sagatave]]" nav pievienoti fakti rītdienai! Lūdzu pievienojiet. --~~~~"""

def putNotif():
	r = pywikibot.data.api.Request(site=site, action='edit', format='json',
										title='Vikipēdija:Administratoru ziņojumu dēlis', section='new', sectiontitle='Nav faktu rītdienai', text=message,token=site.tokens['edit'], summary='Nav faktu rītdienai').submit()#, summary='tests3'
#

nextday = datetime.datetime.now() + datetime.timedelta(days=1)
nextt ='{d.day}'.format(d=nextday)
print(nextt)
newot = doAPI(nextt)
newot = newot.strip()
pywikibot.output(newot)

if newot=='':
	putNotif()