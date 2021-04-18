import re
import pywikibot

site = pywikibot.Site("lv", "wikipedia")

def notify_Edgars():
	page = pywikibot.Page(site,"Dalībnieka diskusija:EdgarsBot")
	pagetext = page.get()
	pagetext += "\n\n{{ping|Edgars2007}} DYK sagatavē divi vienādi datumi --~~~~"
	page.text = pagetext
	page.save(summary="New error", botflag=True)

page = pywikibot.Page(site,'Veidne:Vai tu zināji/Sagatave')
page_text = page.get()

all_dates = re.finditer('<!--(\d+)\. datums\n-->\|\d+=', page_text)

found_dublicate = False

all_date_matches = []

for match in all_dates:
	date = match.group(1)
	if date in all_date_matches:
		found_dublicate = True
		break
	all_date_matches.append(date)

if found_dublicate:
	notify_Edgars()
