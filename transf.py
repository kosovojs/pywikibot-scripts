import pywikibot, re, mwparserfromhell

import wdtools

site = pywikibot.Site("it", "wikipedia")

repo = site.data_repository()

list = """
Found 236 items on PetScan
Working on Obafemi_Martins
Working on Andrea_Carnevale
Working on Francesco_Cozza_(calciatore)
Working on Andrea_De_Marco
Working on Nicola_Rizzoli
Working on Christian_Brighi
Working on Gabriele_Gava
Working on Antonio_Damato
Working on Emidio_Morganti
Working on Paolo_Tagliavento
Working on Saliou_Lassissi
Working on David_Dei
Working on Gianluca_Rocchi
Working on Daniele_Orsato
Working on Mario_Bortolazzi
Working on Julio_César_Ribas
Working on Vincenzo_Esposito_(calciatore_1963)
Working on Evandro_Roncatto
Adding claim
Working on Nicola_Pierpaoli
Working on Ats_Purje
Working on Thomas_Prager
Working on Miguel_Mejía_Barón
Working on Emmerson_Boyce
Working on Mauro_Bergonzi
Working on Sebastiano_Peruzzo
Working on Luca_Banti
Working on Maurizio_Ciampi_(arbitro)
Working on Morten_Berre
Working on João_Paulo_di_Fábio
Working on Carmine_Russo
Working on Massimiliano_Velotto
Working on Renzo_Candussio
Working on Rafael_Marques_Pinto
Working on Chris_James
Working on Murphy_Akanji
Working on Andrea_Gervasoni
Working on Antonio_Giannoccaro
Working on Domenico_Celi
Working on Riccardo_Pinzani
Working on Leonardo_Baracani
Working on Gianpaolo_Calvarese
Working on Paolo_Silvio_Mazzoleni
Working on Nicola_Stefanini
Working on Marco_Guida
Working on Paolo_Valeri
Working on Andrea_Romeo_(arbitro)
Working on Angelo_Martino_Giancola
Working on Daniele_Doveri
Working on Riccardo_Tozzi_(arbitro)
Working on Dino_Tommasi
Working on Arcangelo_Sciannimanico
Working on Roberto_Bagalini
Working on Hannes_Kaasik
Working on Robert_Schörgenhofer
Working on Marijo_Strahonja
Working on Babak_Rafati
Working on Anton_Genov
Working on Cole_Skuse
Working on Davide_Massa
Working on Frans_van_den_Wijngaert
Working on Stefano_Cassarà
Working on Fredrik_Ulvestad
Adding claim
Working on Robin_Dutt
Working on Claudio_Gavillucci
Working on Fabián_Castillo
Working on Gustav_Wikheim
Adding claim
Working on Peter_Sørensen
Adding claim
Working on Jurij_Sëmin
Working on Svein-Erik_Edvartsen
Working on Kjetil_Sælen
Working on Brage_Sandmoen
Working on Luigi_Nasca
Working on Emilio_Ostinelli
Working on Ken_Henry_Johnsen
Working on Trond_Ivar_Døvle
Working on Kristoffer_Helgerud
Working on Anders_Johansen
Working on Silvio_Baratta
Working on Samuel_Bouhours
Working on Ronan_Leaustic
Working on Mark_Beevers
Working on Jordan_Spence
Working on Mikhail_Rosheuvel
Working on Bengt_Eriksen
Working on Anders_Jacobsen_(calciatore)
Working on Dejan_Pavlovic
Working on Dag_Vidar_Hafsås
Working on Serdar_Gözübüyük
Working on Markus_Hameter
Working on Antonio_Barijho
Working on Morten_Christiansen
Working on Neil_Tarrant
Working on Marco_Di_Bello
Working on Fabrizio_Pasqua
Working on Trygve_Kjensli
Working on Koen_Schockaert
Working on Mario_Maurelli
Working on Ede_Herczog
Working on Einar_Halle
Working on Stéphane_Lièvre
Working on Maurizio_Mariani
Working on Angelo_Cervellera
Working on Daniele_Minelli
Working on Davide_Ghersini
Working on Luca_Pairetto
Working on Fabio_Maresca
Working on Erand_Hoxha
Working on Lukas_Kruse
Working on Yoann_Touzghar
Working on Sander_Fischer
Working on Hrvoje_Braović
Working on Alain_Baroja
Working on Michael_Fabbri
Working on Sean_Murray_(calciatore)
Working on Rhian_Dodds
Working on Ola_Hobber_Nilsen
Working on Martin_Lundby
Working on Tore_Hansen
Working on Farouk_Miya
Working on Jacopo_Dall'Oglio
Working on Ivano_Pezzuto
Working on Federico_La_Penna
Working on Juan_Luca_Sacchi
Working on Gianluca_Manganiello
Working on Eugenio_Abbattista
Working on Gianluca_Aureliano
Working on Francesco_Paolo_Saia
Working on Aleandro_Di_Paolo
Working on Rosario_Abisso
Working on Richárd_Vernes
Working on Djai_Essed
Working on Mauricio_Mazzetti
Working on Federico_Furlan
Working on Mathieu_Gorgelin
Working on Masatoshi_Kushibiki
Working on Yūma_Suzuki
Working on Shūhei_Akasaki
Working on Kaoru_Takayama
Working on Yōhei_Ōtake
Working on Daisuke_Kikuchi
Working on Emil_Wahlström
Working on Tomohiko_Murayama
Working on Krzysztof_Kamiński
Working on Shintarō_Kurumaya
Working on Takumi_Abe
Working on Yūki_Sanetō
Working on Masashi_Kamekawa
Working on Taisuke_Nakamura
Working on Nagisa_Sakurauchi
Working on Shun_Morishita
Working on Ashley_Fletcher
Working on Søren_Mussmann
Working on Christoph_Riegler
Working on Royal-Dominique_Fennell
Working on Jacob_Une_Larsson
Working on Juan_Luis_Irazusta
Working on Ryōta_Nagaki
Working on Otar_Kakabadze
Working on Antonio_Tuivuna
Working on Simy
Working on Urban_Žibert
Working on Živko_Atanasov
Working on Dalibor_Radujko
Working on Cruz_Pereira_Sergio
Working on Weverton_Pereira_da_Silva
Working on Matheus_Reis
Working on Lucas_Fernandes
Working on Sérgio_Dutra_Júnior
Working on Edoardo_Lancini
Working on Hyuri
Working on Rafael_Severo_Refatti
no P31, logging
Working on Praneel_Naidu
Working on Saula_Waqa
Working on Narendra_Rao
Working on Gabriele_Matanisiga
Working on Sei_Muroya
Working on Riki_Harakawa
Working on Shin'ya_Yajima
Working on Shōya_Nakajima
Working on Kōsuke_Nakamura
Working on Kim_Min-Tae
Working on Hamza_Barry
Adding claim
Working on Tony_Flygare
Working on Nkhiphitheni_Matombo
Adding claim
Working on David_Boysen
Working on Rafael_Ramos_(calciatore)
Adding claim
Working on Rodrigo_Galo
Adding claim
Working on Mustapha_Carayol
Adding claim
Working on Carlos_Cisneros
Working on Georgemy_Gonçalves
Adding claim
Working on Alex_Lee_(calciatore)
Working on Maximiliano_Uggè
Working on Nuno_Afonso
Working on Oleh_Jaščuk
Working on Patrik_Křap
Working on Gianmarco_Piccioni
Adding claim
Working on Antonio_Čolak
Working on Cristiano_Lombardi
Working on Radoslav_Conev
Working on Pol_Lirola
Working on Nicholas_Ioannou
Working on Kevin_Stewart_(calciatore)
Adding claim
Working on Jamie_Maclaren
Adding claim
Working on Harold_Preciado
Adding claim
Working on Luke_McCormick
Adding claim
Working on Ivan_Petrjak
Adding claim
Working on Matías_Escobar
Adding claim
Working on V″jačeslav_Tankovs'kyj
Adding claim
Working on Myles_Weston
Adding claim
Working on Diego_Rico
Adding claim
Working on Popoola_Saliu
Adding claim
Working on Fred_Friday
Adding claim
Working on Stipe_Bačelić-Grgić
Adding claim
Working on Anthony_Koura
Adding claim
Working on Joe_Cardle
Adding claim
Working on Marco_Festa
Working on Sam_Morsy
Adding claim
Working on Stefano_Padovan
Adding claim
Working on Szymon_Gąsiński
Adding claim
Working on Igor_Mirčeta
Adding claim
Working on Valentin_Cojocaru
Adding claim
Working on Gregor_Bajde
Adding claim
Working on Murilo_Otávio_Mendes
Adding claim
Working on Jakub_Jankto
Adding claim
Working on Leandro_Guaita
Adding claim
Working on Ludvig_Öhman
Working on András_Debreceni
Adding claim
Working on Agustín_Olivera
Adding claim
Working on Silvester_Shkalla
Adding claim
Working on Mostafa_Fathi
Adding claim
Working on Sander_Berge
Adding claim
Working on Pol_García
Adding claim
Working on Stephane_Acka
Adding claim
Working on Omer_Atzili
Adding claim
Working on Cristian_Cigan
Adding claim
Working on Igor_Łasicki
"""

def exclude(list):
	list = list.split('\n')
	list = [el.replace('Working on ','') for el in list if el.startswith('Working on ')]
	
	return list

importedEnWikipedia = pywikibot.Claim(repo,'P143')
enWikipedia = pywikibot.ItemPage(repo,'Q11920')
importedEnWikipedia.setTarget(enWikipedia)

template = "Transfermarkt"
templateCheck = ['transfermarkt']
wdvalueConv = { 'g': 'P2446',#speletajs
				'a': 'P2447',#treneris
				'r': 'P3699'#tiesnesis
}

articles = wdtools.petscan2('BioBot','it','P2446,P2447,P3699',"Transfermarkt")

badarticles = exclude(list)

for article in articles:
	if article in badarticles:
		continue
	
	page = pywikibot.Page(site,article)
	#page = article
	
	if page.namespace() == 0:
		
		item = pywikibot.ItemPage.fromPage(page)
		
		pywikibot.output("Working on %s" % article)
		checkInst = wdtools.checkInstance('P31','Q5',item)
		
		if checkInst==True:
			text = page.get()
			wikicode = mwparserfromhell.parse(text)
			templates = wikicode.filter_templates()
		
			for tpl in templates:
				if tpl.name.lower().strip() in templateCheck:
					if tpl.has("2"):
						sector = tpl.get("2").value.lower().strip()
						if sector in wdvalueConv:
							prop = wdvalueConv[sector]
							if tpl.has("1"):
								id = tpl.get('1').value.strip()
								if len(id)>0:
									
									historycheck = wdtools.checkHist(item,id,prop)
									
									if historycheck==True:
										wdtools.addWD(prop,item,repo,id,importedEnWikipedia)
								
									break
					else:
						prop = 'P2446'
						if tpl.has("1"):
							id = tpl.get('1').value.strip()
							if len(id)>0:
							
							
								historycheck = wdtools.checkHist(item,id,prop)
									
								if historycheck==True:
									wdtools.addWD(prop,item,repo,id,importedEnWikipedia)
							
									break
