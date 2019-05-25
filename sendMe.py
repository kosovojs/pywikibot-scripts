import pywikibot, sys

site = pywikibot.Site("lv", "wikipedia")

scriptName = sys.argv[1] if len(sys.argv) > 1 else "unknown"


page = pywikibot.Page(site,"Dalībnieka diskusija:EdgarsBot")
pagetext = page.get()

pagetext += "\n\n{{{{ping|Edgars2007}}}} {} --~~~~".format(scriptName)


page.text = pagetext
page.save(summary="New error", botflag=True)