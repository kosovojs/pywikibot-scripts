import pywikibot

print(pywikibot.__version__)

lvsite = pywikibot.Site("lv", "wikipedia", user='Edgars2007')

pagetosave = pywikibot.Page(lvsite,'Dalībnieks:Edgars2007/Smilšu kaste')
pagetosave.text = 'test'
pagetosave.save(summary='test', botflag=True)
