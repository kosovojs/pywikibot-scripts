import pywikibot
from datetime import date, timedelta

site = pywikibot.Site("lv", "wikipedia")
site.login()
site.get_tokens('edit')

def doAPI(datestr):
	r = pywikibot.data.api.Request(
		site=site,
		action="expandtemplates",
		format="json",
		text='{{Vai tu zināji/Sagatave|' + datestr + '}}',
		prop='wikitext'
	).submit()

	outputstr = r['expandtemplates']['wikitext']
	return outputstr

message = """{{ping|Biafra|Edgars2007|Papuass|ScAvenger}} lapā "[[Veidne:Vai tu zināji/Sagatave]]" nav pievienoti fakti rītdienai! Lūdzu pievienojiet. --~~~~"""

def putNotif(day_name):
	r = pywikibot.data.api.Request(
		site=site,
		action='edit',
		format='json',
		title='Vikipēdija:Administratoru ziņojumu dēlis',
		section='new',
		sectiontitle='Nav faktu rītdienai ({})'.format(day_name),
		text=message,
		token=site.tokens['edit'],
		summary='Nav faktu rītdienai'
	).submit()

yesterday = date.today() + timedelta(1)
nextday = yesterday.strftime('%Y-%m-%d')
newot = doAPI(nextday)
newot = newot.strip()

if newot == '':
	putNotif(nextday)
