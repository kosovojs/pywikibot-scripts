import pywikibot, re
import toolforge

site = pywikibot.Site('lv', "wikipedia")
conn = toolforge.connect('lvwiki_p')

#data = get_quarry('4861')

SQL = """SELECT #page_title, tl_title
p.page_title, COUNT(lt_title)
FROM templatelinks t
join linktarget ON tl_target_id = lt_id
join page p on p.page_id = t.tl_from
INNER JOIN categorylinks c ON p.page_id = c.cl_from AND c.cl_to = 'Visi_Vikipēdijas_uzlabojamie_raksti'
where lt_namespace = 10 AND lt_title IN ("Dzēst", "Dzēst+", "Apvienot", "Apšaubīts", "Atdalīt", "Atjaunināt", "Atsauces+", "Atsevišķs_raksts", "Atveidošana", "Autobiogrāfija", "Autortiesību_problēmas", "Autortiesību_problēmas_(maza)", "Eksperts", "Enciklopēdisks_stils", "Infokaste+", "Izolēts_raksts", "Jāuzlabo", "Jāpārraksta", "Kategorija_jādala", "Ievads+", "Kategorijas+", "Konfl", "Informācijas_izklāsts", "Neatkarīgas_atsauces+", "Nepilnīgs", "Nenozīmīgs", "Nepieciešama_atsauce", "Nepieciešama_dokumentācija", "Nepilnīga_nodaļa", "Noformējums+", "Novecojis_sastāvs", "Novecojusi_saite", "Papildu_atsauces+", "Pareizrakstība", "Pārrakstīt", "Pov", "Sadalīt", "Sadaļas+", "Saistīts_teksts", "Slikts_tulkojums", "Starpviki+", "Teksts+", "Under_construction", "Viens_avots", "Vikisaites+", "Svešvaloda")
		and tl_from_namespace=0 and page_is_redirect=0
GROUP BY p.page_title
ORDER BY COUNT(lt_title) DESC
LIMIT 300"""

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query():
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(SQL)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows
#
data = run_query()


rows = []
articles = []

for article in data:
	article = [encode_if_necessary(f) for f in article]
	art, cats = article
	rows.append('|-\n| [[{}]] || {}'.format(art.replace('_',' '), cats))
	articles.append('| [[{}]]'.format(art.replace('_',' ')))
#
heading = """{{Dalībnieks:Edgars2007/Pieprasīt datu atjaunošanu}}
Šajā lapā apkopoti tie raksti, kam ir vismaz 3 uzlabošanas veidnes. Saraksts nav pilnīgs.

{| class="wikitable sortable"
|-
! Raksta nosaukums !! Uzlabošanas veidņu skaits{{efn|Pašlaik tikušas ņemtas vērā šīs uzlabošanas veidnes: {{tl|Dzēst}}, {{tl|Dzēst+}}, {{tl|Apvienot}}, {{tl|Apšaubīts}}, {{tl|Atdalīt}}, {{tl|Atjaunināt}}, {{tl|Atsauces+}}, {{tl|Atsevišķs raksts}}, {{tl|Atveidošana}}, {{tl|Autobiogrāfija}}, {{tl|Autortiesību problēmas}}, {{tl|Autortiesību problēmas (maza)}}, {{tl|Eksperts}}, {{tl|Enciklopēdisks stils}}, {{tl|Infokaste+}}, {{tl|Izolēts raksts}}, {{tl|Jāuzlabo}}, {{tl|Jāpārraksta}}, {{tl|Ievads+}}, {{tl|Kategorijas+}}, {{tl|Konfl}}, {{tl|Informācijas izklāsts}}, {{tl|Neatkarīgas atsauces+}}, {{tl|Nepilnīgs}}, {{tl|Nenozīmīgs}}, {{tl|Nepieciešama atsauce}}, {{tl|Nepilnīga nodaļa}}, {{tl|Noformējums+}}, {{tl|Novecojis sastāvs}}, {{tl|Novecojusi saite}}, {{tl|Papildu atsauces+}}, {{tl|Pareizrakstība}}, {{tl|Pārrakstīt}}, {{tl|Pov}}, {{tl|Sadalīt}}, {{tl|Sadaļas+}}, {{tl|Saistīts teksts}}, {{tl|Slikts tulkojums}}, {{tl|Starpviki+}}, {{tl|Teksts+}}, {{tl|Viens avots}}, {{tl|Vikisaites+}}, {{tl|Svešvaloda}}<!-- {{tl|Kategorija jādala}}, {{tl|Nepieciešama dokumentācija}}, {{tl|Under construction}}, , {{tl|Ienākošās saites}}, {{tl|Novecojusi veidne}} -->. Ja esi pamanījis kādu uzlabošanas veidni, kas nav šajā sarakstā, paziņo to diskusiju lapā.<!--sports update; -->}}
"""

end = """

== Piezīmes ==
{{notelist}}

[[Kategorija:Vikipēdijas uzlabošanas vikiprojekts]]"""

rowsfsdf = heading + '\n'.join(rows) + '\n|}' + end
'''
filsesave = open('badarticles withoutfdgdfgdfgdfg real cats-1.txt', "w", encoding='utf-8')
filsesave.write(rowsfsdf)

filsesave2 = open('badarticles withoutfdgdfgdfgdfg real catgfdgfgs-1.txt', "w", encoding='utf-8')
filsesave2.write('\n'.join(articles))
'''

page = pywikibot.Page(site,'Vikiprojekts:Vikipēdijas uzlabošana/Raksti/Raksti, kuros ir visvairāk uzlabošanas veidņu')
oldtxt = page.get()

page.text = rowsfsdf
page.save(comment='Bots: atjaunināts saraksts', botflag=False, minor=False)
