import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

site = pywikibot.Site("en", "wikipedia")
conn_fr = toolforge.connect('frwiki_p','analytics')
conn_ru = toolforge.connect('ruwiki_p','analytics')
#connLabs = toolforge.connect_tools('s53143__mis_lists_p')
#cursor1 = connLabs.cursor()

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection = conn_fr):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = connection.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows
#
SQL_main = """select count(l.ll_lang) as langs, p.page_title, (select m2.ll_title from langlinks m2 where m2.ll_from=l.ll_from and m2.ll_lang="en")  as en, (select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd{}
from langlinks l
join page p on p.page_id=l.ll_from
and p.page_namespace=0 and not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
	and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
               										and cla.cl_to="Portail:{}/Articles_liés"
               )
group by l.ll_from
having count(l.ll_lang)>20
order by count(l.ll_lang) desc;"""

def format_frwiki(infoboxname,data):

	ret = []
	for row in data:
		if infoboxname=='indija':
			langs,fr,en,wd,infobox = row

			if not infobox:
				infobox = ''
			infs = infobox.split('|')

			if 'Infobox_Subdivision_administrative' in infs: continue
			if 'Infobox_Biographie2' in infs: continue
			if 'Infobox_Politicien' in infs: continue


		else:
			langs,fr,en,wd = row

		if en!='':
			ret.append([en,langs,wd])
		else:
			pywikibot.output(row)
	return ret
#
def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

#infoboxlist = infoboxlist[::-1]

#sql_insert = 'UPDATE `entries` INTO (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'
sql_update = 'UPDATE `entries` SET jsondata=%s, last_upd=%s where group_name=%s and name=%s'


def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def get_page_info_chunk(SQL,additional,pages,connectionObject):
	query_res = run_query(SQL.format(additional,', '.join(map(str,pages))),connectionObject)
	query_res = [encode_all_items(f) for f in query_res]

	query_res = {f[0]:f[1:] for f in query_res}

	return query_res
#
def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#
def checkTitle(project, page_data):
	project = project.lower().replace(' ','_')
	title = page_data[1].replace('_',' ')


	if project == "monde_antique":
		if re.search('^(AD )?\d+s?(\sBC)?',title):
			return False
	elif project == "monde_indien":
		infoboxes = page_data[3].replace('_',' ')
		if not infoboxes:
			infoboxes = ""

		infs = infobox.split('|')

		if 'Infobox_Subdivision_administrative' in infs: return False
		if 'Infobox_Biographie2' in infs: return False
		if 'Infobox_Politicien' in infs: return False
	elif project == "japon":
		infoboxes = page_data[3].replace('_',' ')
		if not infoboxes:
			infoboxes = ""

		infs = infobox.split('|')

		if 'Infobox Localité' in infs: return False
		#if 'Infobox_Biographie2' in infs: return False
		#if 'Infobox_Politicien' in infs: return False

	return True

def merge_res(iw_mas,info,project):
	final = []
	errors = []

	for page_id in iw_mas:
		if page_id not in info:
			errors.append([page_id,iws])
			continue

		iws = iw_mas[page_id]

		page_info = info[page_id]

		if page_info[1]==None:#no enwiki title
			continue

		isValidTitle = True

		if project in ['Monde antique']:
			isValidTitle = checkTitle(project,page_info)

		if isValidTitle:
			curr_item = [page_info[1],iws,page_info[2]]
			final.append(curr_item)
	#
	a = sorted(final, key=lambda x: -int(x[1]))

	return [a,errors]
#
def get_page_info(project,pages,connectionObject):
	alldata = {}
	addit = ""

	SQL = """select page_id, page_title,
	(select m2.ll_title from langlinks m2 where m2.ll_from=p.page_id and m2.ll_lang="en")  as en,
	(select pp.pp_value from page_props pp where pp.pp_page=p.page_id and pp_propname='wikibase_item') as wd{}
	from page p
	where p.page_namespace=0 and p.page_is_redirect=0 and p.page_id in ({})"""

	if project=='Monde_indien':
		addit = ",    (SELECT GROUP_CONCAT(tl_title SEPARATOR '|') FROM templatelinks            WHERE tl_title like 'Infobox%' and tl_namespace = 10 and tl_from=p.page_id) as box"

	for chunk in chunker(pages, 50):
		thispart = get_page_info_chunk(SQL,addit,chunk,connectionObject)
		alldata.update(thispart)
	#
	return alldata
#
def one_project(project,connectionObject):
	number = "2000" if project=="Monde antique" else "1000"

	SQL = """select count(l.ll_lang) as langs, ll_from
		from langlinks l
		where not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
			and exists (select * from categorylinks cla where cla.cl_type="page" and l.ll_from=cla.cl_from
															and cla.cl_to="Portail:{}/Articles_liés"
					   )
		group by l.ll_from
		order by count(l.ll_lang) desc
	limit {};""".format(project.replace(' ','_'),number)

	query_res = run_query(SQL, connectionObject)
	query_res = [encode_all_items(f) for f in query_res]

	page_ids = {f[1]:f[0] for f in query_res}

	page_info = get_page_info(project,list(page_ids),connectionObject)

	finaldata, errors = merge_res(page_ids,page_info,project)

	finaldata = str(json.dumps(finaldata[:800]))#finaldata[:800]

	#with open("tokija-ex.txt", "w", encoding='utf-8') as file1:
	#	file1.write(str(finaldata))
	return finaldata
#
def one_project_tpl(project,connectionObject):
	number = "2000" if project=="Monde antique" else "1000"

	SQL = """select count(l.ll_lang) as langs, ll_from
from langlinks l
where not exists (select * from langlinks m where m.ll_from=l.ll_from and m.ll_lang="lv")
	and exists (select * from templatelinks tl where l.ll_from=tl.tl_from and tl_namespace=10 and tl.tl_from_namespace=0
               										and tl.tl_title="{}"
               )
group by l.ll_from
order by count(l.ll_lang) desc
limit {};""".format(project.replace(' ','_'),number)

	query_res = run_query(SQL,connectionObject)
	query_res = [encode_all_items(f) for f in query_res]

	page_ids = {f[1]:f[0] for f in query_res}

	page_info = get_page_info(project,list(page_ids),connectionObject)

	finaldata, errors = merge_res(page_ids,page_info,project)

	finaldata = str(json.dumps(finaldata[:800]))#finaldata[:800]

	#with open("tokija-ex.txt", "w", encoding='utf-8') as file1:
	#	file1.write(str(finaldata))
	return finaldata
#
def insert_into_db(group_name,name,jsondata):
	sql_insert = 'INSERT INTO `entries` (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'
	sql_update = 'UPDATE `entries` SET jsondata=%s, last_upd=%s where group_name=%s and name=%s'

	curr_time = utc_to_local(datetime.utcnow())
	dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)

	connLabs = toolforge.connect_tools('s53143__mis_lists_p')
	cursor1 = connLabs.cursor()

	isAlreadyInDB_sql = 'select id from entries where group_name=%s and name=%s'

	cursor1.execute(isAlreadyInDB_sql, (group_name,name))
	isAlreadyInDB = cursor1.fetchall()

	#cursor1.execute(sql_insert, (infobox.replace('Infobox_','').replace('_',' '), 'eninfobox',str(json.dumps(result_json)),dateforq1))
	if len(isAlreadyInDB)<1:
		cursor1.execute(sql_insert, (name, group_name,jsondata,dateforq1))
	else:
		cursor1.execute(sql_update, (jsondata,dateforq1,group_name, name))

	connLabs.commit()
	connLabs.close()
#

jsoninput = [
	{'group':'other','name':'Monuments','template':'Infobox_Monument','lang':conn_fr},
	{'group':'other','name':'Gratte-ciel','template':'Infobox_Gratte-ciel','lang':conn_fr},
	{'group':'other','name':'Geoobjekti','template':'Геокар','lang':conn_ru},
	{'group':'other','name':'Reliģiskas ēkas','template':'Культовое сооружение','lang':conn_ru},
	{'group':'other','name':'Apskates vietas','template':'Достопримечательность','lang':conn_ru},
	#{'group':'other','name':'BLR','template':None, 'portalFr':'Biélorussie','lang':conn_fr},
]

def main():
	#infoboxlist = get_input_list()

	for infobox in jsoninput:
		infname = infobox['name']
		languageWiki = infobox['lang']
		template = infobox['template']
		portalFr = infobox['portalFr'] if 'portalFr' in infobox else None
		grupa = infobox['group']
		pywikibot.output('\t'+infname)

		if portalFr:
			result_json = one_project(portalFr,languageWiki)
		else:
			result_json = one_project_tpl(template,languageWiki)
		insert_into_db(grupa,infname,result_json)

	conn_ru.close()
	conn_fr.close()
	pywikibot.output('done')
#

fr_infobox_list = [
	"Infobox_2_euros", "Infobox_API", "Infobox_Abbaye", "Infobox_Abbaye_cistercienne", "Infobox_Accident_de_transport", "Infobox_Adhésion_à_l'Union_européenne", "Infobox_Adresse_monarchique", "Infobox_Affaire_criminelle", "Infobox_Agence_européenne", "Infobox_Agence_gouvernementale", "Infobox_Agence_spatiale", "Infobox_Agglomération_du_Québec", "Infobox_Agriculture", "Infobox_Aire_protégée", "Infobox_Algorithme", "Infobox_Algorithme2", "Infobox_Alliance_aérienne", "Infobox_Alliance_politique_française", "Infobox_Alliance_politique_indienne", "Infobox_Alpiniste,_grimpeur", "Infobox_Alsace", "Infobox_Amphithéâtre_Rome_Antique", "Infobox_Amphoe", "Infobox_Amt_du_Danemark", "Infobox_Aménagement_cyclable", "Infobox_Anarchisme_par_zone_géographique", "Infobox_Anatomie", "Infobox_Ancien_arrondissement_du_Royaume-Uni", "Infobox_Ancienne_commune", "Infobox_Ancienne_commune_de_France", "Infobox_Ancienne_commune_des_Pays-Bas", "Infobox_Ancienne_commune_du_Danemark", "Infobox_Ancienne_commune_du_Luxembourg", "Infobox_Ancienne_entité_territoriale", "Infobox_Ancienne_municipalité_canadienne", "Infobox_Animal", "Infobox_Animal_dans_la_culture", "Infobox_Animateur_audiovisuel", "Infobox_Animation_et_bande_dessinée_asiatiques", "Infobox_Année_en_astronomie", "Infobox_Appareil_informatique", "Infobox_Appareil_photo_argentique", "Infobox_Appareil_photo_numérique", "Infobox_Appellation_d'origine", "Infobox_Appellation_de_pomme_de_terre", "Infobox_Apskritis_de_Lituanie", "Infobox_Arbitre", "Infobox_Arbre_remarquable", "Infobox_Archer", "Infobox_Archidiocèse_catholique", "Infobox_Architecte", "Infobox_Architecture_CPU", "Infobox_Architecture_logicielle", "Infobox_Archives", "Infobox_Archéologue", "Infobox_Aristocrate", "Infobox_Aristocrate_médiéval", "Infobox_Arme", "Infobox_Armoiries", "Infobox_Armée", "Infobox_Arrondissement_administratif_de_Belgique", "Infobox_Arrondissement_d'Allemagne", "Infobox_Arrondissement_d'Haïti", "Infobox_Arrondissement_de_France", "Infobox_Arrondissement_judiciaire_de_Belgique", "Infobox_Arrondissement_judiciaire_du_Luxembourg", "Infobox_Arrondissement_municipal_français", "Infobox_Arrêt_de_la_Cour_suprême_des_États-Unis", "Infobox_Arsenal_nucléaire", "Infobox_Art", "Infobox_Art_martial", "Infobox_Artillerie", "Infobox_Artiste", "Infobox_Artiste_martial", "Infobox_Artère", "Infobox_Artéfact_archéologique", "Infobox_Arènes", "Infobox_Assemblée", "Infobox_Assemblée_délibérante_de_France", "Infobox_Association", "Infobox_Associations_etudiantes", "Infobox_Astre", "Infobox_Atelier_ferroviaire", "Infobox_Athlète", "Infobox_Atmosphère", "Infobox_Attentat", "Infobox_Attractions", "Infobox_Auteur_de_livre-jeu", "Infobox_Autogire", "Infobox_Automobile", "Infobox_Avion", "Infobox_Avion_léger", "Infobox_Avion_militaire", "Infobox_Aéronef_radiocommandé", "Infobox_Aéroport", "Infobox_Aérostat", "Infobox_BTS", "Infobox_BUT", "Infobox_Baladodiffusion", "Infobox_Bande_dessinée", "Infobox_Bande_indienne", "Infobox_Banque", "Infobox_Banque_centrale", "Infobox_Barrage", "Infobox_Base_de_lancement", "Infobox_Base_militaire", "Infobox_Base_militaire_avec_aéroport", "Infobox_Base_permanente", "Infobox_Bassin_hydrographique", "Infobox_Bassin_minier", "Infobox_Bassin_sédimentaire", "Infobox_Bassin_versant", "Infobox_Batteries", "Infobox_Bibliographie", "Infobox_Bibliothèque", "Infobox_Bilan_club_de_football_européen", "Infobox_Bilan_club_de_rugby_à_XV_européen", "Infobox_Bilan_sportif", "Infobox_Bilan_équipe_nationale", "Infobox_Bilan_équipe_nationale_volley-ball", "Infobox_Billet", "Infobox_Binaire_X", "Infobox_Biographie", "Infobox_Biographie2", "Infobox_Biographie_bouddhiste", "Infobox_Biohomonymie", "Infobox_Biome", "Infobox_Bière", "Infobox_Blindé", "Infobox_Bloc_de_programmation_TV", "Infobox_Boisson", "Infobox_Bombe", "Infobox_Bourse", "Infobox_Boxeur", "Infobox_Brasserie", "Infobox_Bretagne", "Infobox_Budget", "Infobox_Bundesautobahn", "Infobox_Béarn", "Infobox_CART_World_Series", "Infobox_CBT", "Infobox_CPGE", "Infobox_Calculatrice_Casio", "Infobox_Calculatrice_TI", "Infobox_Camp_de_concentration", "Infobox_Camping", "Infobox_Campus", "Infobox_Canal", "Infobox_Canal_ionique", "Infobox_Cantate_Bach", "Infobox_Canton_d'Équateur", "Infobox_Canton_de_France", "Infobox_Canton_de_Suisse", "Infobox_Canton_du_Costa_Rica", "Infobox_Canton_du_Luxembourg", "Infobox_Canton_québécois", "Infobox_Cap", "Infobox_Caractère_Unicode", "Infobox_Carnaval", "Infobox_Carte_à_jouer", "Infobox_Cartouche", "Infobox_Casino", "Infobox_Catch_(personnalité)", "Infobox_Catch_(spectacle)", "Infobox_Catch_(spectacles)", "Infobox_Catch_(titre)", "Infobox_Catch_(équipe)", "Infobox_Catcheur", "Infobox_Catholicos_de_l'Église_apostolique_arménienne", "Infobox_Cavalier", "Infobox_Cave_vinicole", "Infobox_Caïdat_ou_cercle_du_Maroc", "Infobox_Centrale", "Infobox_Centrale_nucléaire", "Infobox_Centre_commercial", "Infobox_Centre_de_congrès", "Infobox_Cercle_du_Mali", "Infobox_Chambre_de_commerce", "Infobox_Champ_d'hydrocarbures", "Infobox_Championnat_d'échecs", "Infobox_Championnats_de_karaté", "Infobox_Chanson", "Infobox_Chart", "Infobox_Charte_Lyon", "Infobox_Chaîne_de_télévision", "Infobox_Chemin_de_fer_touristique", "Infobox_Cheminée", "Infobox_Cheptel", "Infobox_Cheval", "Infobox_Chiffrement_par_bloc", "Infobox_Chimie", "Infobox_Chute_d'eau", "Infobox_Châssis_sport-automobile", "Infobox_Châtaignier", "Infobox_Château", "Infobox_Cimetière", "Infobox_Cinéma_(caméra)", "Infobox_Cinéma_(festival)", "Infobox_Cinéma_(film)", "Infobox_Cinéma_(personnalité)", "Infobox_Cinéma_(projecteur)", "Infobox_Cinéma_(studio)", "Infobox_Cinéma_(série_de_films)", "Infobox_Circonscription_de_Paris", "Infobox_Circonscription_de_Tunisie", "Infobox_Circonscription_et_région_électorale_du_Parlement_gallois", "Infobox_Circonscription_législative_française", "Infobox_Circonscription_législative_marocaine", "Infobox_Circonscription_électorale", "Infobox_Circonscription_électorale_d'Écosse", "Infobox_Circonscription_électorale_de_Hongrie", "Infobox_Circonscription_électorale_de_Turquie", "Infobox_Circonscription_électorale_du_Canada", "Infobox_Circonscription_électorale_du_Luxembourg", "Infobox_Circonscription_électorale_du_Royaume-Uni", "Infobox_Circonscription_électorale_française", "Infobox_Circonscriptions_de_l'Assemblée_de_Londres", "Infobox_Circonscriptions_des_îles_Cook", "Infobox_Circuit_automobile", "Infobox_Cirque_naturel", "Infobox_Clan", "Infobox_Classe_de_paquebots", "Infobox_Classe_navire_de_guerre", "Infobox_Classement_musical", "Infobox_Club_d'aviron", "Infobox_Club_d'escrime", "Infobox_Club_de_baseball", "Infobox_Club_de_basket-ball", "Infobox_Club_de_canoë-kayak", "Infobox_Club_de_floorball", "Infobox_Club_de_football", "Infobox_Club_de_gymnastique", "Infobox_Club_de_handball", "Infobox_Club_de_karaté", "Infobox_Club_de_natation", "Infobox_Club_de_rink_hockey", "Infobox_Club_de_rugby", "Infobox_Club_de_sports_gaéliques", "Infobox_Club_de_tir_à_l'arc", "Infobox_Club_de_volley-ball", "Infobox_Club_nautique", "Infobox_Club_omnisports", "Infobox_Club_sportif", "Infobox_Club_universitaire", "Infobox_Cocktail", "Infobox_Codage_de_caractères", "Infobox_Col", "Infobox_Collectif_(artistes)", "Infobox_Collection_de_livre-jeu", "Infobox_Collectivité_de_la_république_démocratique_du_Congo", "Infobox_Comarque_d'Espagne", "Infobox_Combat_de_boxe", "Infobox_Combiné_nordique", "Infobox_Combiné_nordique_2", "Infobox_Comic_book", "Infobox_Comitat_de_Croatie", "Infobox_Comitat_de_Hongrie", "Infobox_Comitat_du_Royaume_de_Hongrie", "Infobox_Commanderie", "Infobox_Commanderie_hospitalière", "Infobox_Commanderie_templière", "Infobox_Commission_européenne", "Infobox_Commission_parlementaire_française", "Infobox_Communauté_autonome_d'Espagne", "Infobox_Communauté_d'Arménie", "Infobox_Communauté_de_Belgique", "Infobox_Communauté_du_Haut-Karabagh", "Infobox_Commune_d'Algérie", "Infobox_Commune_d'Allemagne", "Infobox_Commune_d'Argentine", "Infobox_Commune_d'Autriche", "Infobox_Commune_d'Espagne", "Infobox_Commune_d'Irak", "Infobox_Commune_d'Iran", "Infobox_Commune_d'Italie", "Infobox_Commune_d'Oman", "Infobox_Commune_d'Ouganda", "Infobox_Commune_d'Égypte", "Infobox_Commune_de_Belgique", "Infobox_Commune_de_Chypre", "Infobox_Commune_de_Côte_d'Ivoire", "Infobox_Commune_de_France", "Infobox_Commune_de_Géorgie", "Infobox_Commune_de_Hongrie", "Infobox_Commune_de_Mauritanie", "Infobox_Commune_de_Norvège", "Infobox_Commune_de_Roumanie", "Infobox_Commune_de_Slovaquie", "Infobox_Commune_de_Somalie", "Infobox_Commune_de_Somaliland", "Infobox_Commune_de_Suisse", "Infobox_Commune_de_Suède", "Infobox_Commune_de_la_république_du_Congo", "Infobox_Commune_de_la_république_démocratique_du_Congo", "Infobox_Commune_des_Pays-Bas", "Infobox_Commune_du_Bhoutan", "Infobox_Commune_du_Bénin", "Infobox_Commune_du_Cameroun", "Infobox_Commune_du_Chili", "Infobox_Commune_du_Danemark", "Infobox_Commune_du_Groenland", "Infobox_Commune_du_Liban", "Infobox_Commune_du_Liechtenstein", "Infobox_Commune_du_Luxembourg", "Infobox_Commune_du_Mali", "Infobox_Commune_du_Mexique", "Infobox_Commune_du_Nicaragua", "Infobox_Commune_du_Nigeria", "Infobox_Commune_du_Portugal", "Infobox_Commune_du_Tchad", "Infobox_Commune_rurale_du_Maroc", "Infobox_Compagnie_aérienne", "Infobox_Compagnie_ferroviaire", "Infobox_Comparatif_UE-puissances_émergentes", "Infobox_Composant_ISS", "Infobox_Composé_chimique", "Infobox_Compteur_exoplanètes", "Infobox_Compétition_de_go", "Infobox_Compétition_de_sport_électronique", "Infobox_Compétition_musicale", "Infobox_Compétition_sportive", "Infobox_Comté_d'Angleterre", "Infobox_Comté_d'Irlande", "Infobox_Comté_de_Norvège", "Infobox_Comté_de_Suède", "Infobox_Comté_de_l'Île-du-Prince-Édouard", "Infobox_Comté_des_États-Unis", "Infobox_Comète", "Infobox_Comédie_musicale", "Infobox_Concept_historique", "Infobox_Concept_socio-fiscal", "Infobox_Concert_du_nouvel_an", "Infobox_Concession_du_Bassin_minier_du_Nord-Pas-de-Calais", "Infobox_Concession_ferroviaire_britannique", "Infobox_Concile", "Infobox_Conclave", "Infobox_Concours_Eurovision_Asie_de_la_chanson", "Infobox_Concours_Eurovision_de_la_chanson", "Infobox_Concours_miss", "Infobox_Configuration_minimum", "Infobox_Configuration_recommandée", "Infobox_Conflit_militaire", "Infobox_Congrès_des_États-Unis", "Infobox_Congrès_politique", "Infobox_Conjoint_politique", "Infobox_Connectique", "Infobox_Conseil_du_roi", "Infobox_Conseil_départemental", "Infobox_Conseil_européen", "Infobox_Conseil_régional_d'Israël", "Infobox_Conseil_scolaire_au_Canada", "Infobox_Console_de_jeux_vidéo", "Infobox_Constellation", "Infobox_Conte_populaire", "Infobox_Continent", "Infobox_Convention", "Infobox_Convoi_de_déportation", "Infobox_Convois_WWII", "Infobox_Couleur", "Infobox_Council_area", "Infobox_Coupe_Grey", "Infobox_Cour_de_cassation_(France)", "Infobox_Cours_d'eau", "Infobox_Course_cycliste", "Infobox_Course_de_Formule_1", "Infobox_Course_de_NASCAR", "Infobox_Course_de_Rallycross", "Infobox_Course_de_WTCC", "Infobox_Course_hippique", "Infobox_Cratère", "Infobox_Criminel", "Infobox_Critique_presse", "Infobox_Croisade", "Infobox_Cryptomonnaie", "Infobox_Créature", "Infobox_Cuisines_du_monde", "Infobox_Cycle_solaire", "Infobox_Cycliste", "Infobox_Cycliste_Bac_à_sable", "Infobox_Cycliste_Wikidata", "Infobox_Cyclone", "Infobox_Cyclone_résumé", "Infobox_Cégep", "Infobox_Célébration", "Infobox_Cépage", "Infobox_Cérémonie", "Infobox_Côte", "Infobox_DROM-COM", "Infobox_Dalaï-lama", "Infobox_Danse_(compagnie)", "Infobox_Danse_(œuvre)", "Infobox_Daïra_d'Algérie", "Infobox_Deaflympics", "Infobox_Descriptif_course_cycliste", "Infobox_Deux_écrivains", "Infobox_Diffusion", "Infobox_Diocèse_catholique", "Infobox_Discipline", "Infobox_Discours", "Infobox_Disque_circumstellaire", "Infobox_Distillerie", "Infobox_Distinction", "Infobox_Distribution_statistiques", "Infobox_District_congrès_US", "Infobox_District_d'Allemagne", "Infobox_District_d'Angleterre", "Infobox_District_d'Autriche", "Infobox_District_d'Irlande_du_Nord", "Infobox_District_d'Israël", "Infobox_District_d'Ouganda", "Infobox_District_de_Bogota", "Infobox_District_de_Londres", "Infobox_District_de_Madagascar", "Infobox_District_de_Russie", "Infobox_District_de_Slovaquie", "Infobox_District_de_Suisse", "Infobox_District_de_Tanzanie", "Infobox_District_de_Tchéquie", "Infobox_District_de_la_république_démocratique_du_Congo", "Infobox_District_du_Bangladesh", "Infobox_District_du_Botswana", "Infobox_District_du_Brésil", "Infobox_District_du_Ghana", "Infobox_District_du_Kazakhstan", "Infobox_District_du_Kenya", "Infobox_District_du_Kosovo", "Infobox_District_du_Liberia", "Infobox_District_du_Luxembourg", "Infobox_District_du_Pakistan", "Infobox_District_du_Portugal", "Infobox_District_du_Rwanda", "Infobox_District_du_Viêt_Nam", "Infobox_District_fédéral_de_Russie", "Infobox_District_indien", "Infobox_Divinité", "Infobox_Divinité_des_Royaumes_oubliés", "Infobox_Division_administrative_de_Corée_du_Nord", "Infobox_Division_administrative_de_Corée_du_Sud", "Infobox_Division_du_Bangladesh", "Infobox_Division_sénatoriale_du_Canada", "Infobox_Document", "Infobox_Document_d'identité", "Infobox_Document_juridique_du_haut_Moyen_Âge", "Infobox_Document_pontifical", "Infobox_Domaine_de_premier_niveau", "Infobox_Double_confrontation_de_football", "Infobox_Draft", "Infobox_Drapeau", "Infobox_Droits_LGBT", "Infobox_Drone_civil", "Infobox_Duel_de_montagnes_russes", "Infobox_Dème_de_Grèce", "Infobox_Décharge", "Infobox_Décision_de_la_Cour_suprême_du_Canada", "Infobox_Décision_juridique", "Infobox_Déités_D&D", "Infobox_Délégation_tunisienne", "Infobox_Démographie", "Infobox_Dénomination_anatomique", "Infobox_Dénomination_chrétienne", "Infobox_Département_d'Argentine", "Infobox_Département_d'Haïti", "Infobox_Département_d'Uruguay", "Infobox_Département_de_Colombie", "Infobox_Département_de_Côte_d'Ivoire", "Infobox_Département_de_France", "Infobox_Département_du_Burkina_Faso", "Infobox_Département_du_Bénin", "Infobox_Département_du_Cameroun", "Infobox_Département_du_Gabon", "Infobox_Département_du_Paraguay", "Infobox_Département_du_Salvador", "Infobox_Département_du_Sénégal", "Infobox_Département_du_Tchad", "Infobox_Départements_de_l'administration_américaine", "Infobox_Députations_provinciales_d'Espagne", "Infobox_Députés_département", "Infobox_Désert", "Infobox_Empereur_de_Chine", "Infobox_Empereur_romain", "Infobox_Encyclopédie", "Infobox_Engin_spatial", "Infobox_Engin_spatial_auxiliaire", "Infobox_Enzyme", "Infobox_Equipe_MotoGP", "Infobox_Erreur_syntaxique", "Infobox_Escrimeur", "Infobox_Espace_public", "Infobox_Espace_vert", "Infobox_Espace_vert2", "Infobox_Essai_nucléaire", "Infobox_Eurovision", "Infobox_Eurovision_Asie", "Infobox_Exolune", "Infobox_Exoplanète", "Infobox_Explorateur", "Infobox_Exposition", "Infobox_Exposition_internationale", "Infobox_Expédition_ISS", "Infobox_Faciès_culturel", "Infobox_Facteur_de_la_coagulation", "Infobox_Faction_armée", "Infobox_Famille_Pokémon", "Infobox_Famille_de_protéines", "Infobox_Famille_noble", "Infobox_Famine", "Infobox_Feu_de_forêt", "Infobox_Figure_historique_des_Trois_Royaumes", "Infobox_Flandre", "Infobox_Flipper", "Infobox_Foire", "Infobox_Fonction_mathématique", "Infobox_Fonte", "Infobox_Footballeur", "Infobox_Format_de_données", "Infobox_Formation_rocheuse", "Infobox_Fort_romain", "Infobox_Fortification_Séré_de_Rivières", "Infobox_Forêt", "Infobox_Fossile", "Infobox_Franchise_LCF", "Infobox_Franchise_MLB", "Infobox_Frazione", "Infobox_Freguesia_du_Portugal", "Infobox_Fromage", "Infobox_Frontière", "Infobox_Fruit", "Infobox_Fuite_d'information", "Infobox_Fuseau_horaire", "Infobox_Fusée", "Infobox_Fusée-sonde", "Infobox_Fusée_Redstone", "Infobox_Fédération_sportive", "Infobox_GPU", "Infobox_Galaxie", "Infobox_Galaxie_Groupe_Local", "Infobox_Gare", "Infobox_Gasconha", "Infobox_Gens", "Infobox_Glacier", "Infobox_Glyphe_phénicien", "Infobox_Gmina_de_Pologne", "Infobox_Golfeur", "Infobox_Gorge", "Infobox_Gouvernement", "Infobox_Gouvernement_autonomique_d'Espagne", "Infobox_Gouvernement_territorial", "Infobox_Gouverneur_de_la_Régence_d'Alger", "Infobox_Gouvernorat_tunisien", "Infobox_Grade", "Infobox_Grand_Prix_moto", "Infobox_Grande_région_suisse", "Infobox_Grandeur_physique", "Infobox_Graphe", "Infobox_Graphème", "Infobox_Gratte-ciel", "Infobox_Grotte", "Infobox_Groupe_de_musique", "Infobox_Groupe_ethnique", "Infobox_Groupe_parlementaire", "Infobox_Groupe_parlementaire_d'Espagne", "Infobox_Groupe_parlementaire_d'un_conseil_départemental", "Infobox_Groupe_parlementaire_d'un_conseil_régional", "Infobox_Groupement_de_collectivités_européennes", "Infobox_Guitare", "Infobox_Gymnaste", "Infobox_Géants_de_processions_et_de_cortèges", "Infobox_Géants_du_Nord-Pas-de-Calais", "Infobox_Géographie_d'Io", "Infobox_Géographie_de_(1)_Cérès", "Infobox_Géographie_de_(4)_Vesta", "Infobox_Géographie_de_Charon", "Infobox_Géographie_de_Mars", "Infobox_Géographie_de_Neptune", "Infobox_Géographie_de_Pluton", "Infobox_Géographie_de_Titan", "Infobox_Géographie_de_Triton", "Infobox_Géographie_de_Vénus", "Infobox_Géographie_nationale", "Infobox_Géographie_planétaire", "Infobox_Géologie_régionale", "Infobox_Géométrie_moléculaire", "Infobox_Halakha", "Infobox_Handballeur", "Infobox_Haplogroupe", "Infobox_Hippodrome", "Infobox_Histoire_de_la_bande_dessinée", "Infobox_Histoire_du_sport", "Infobox_Historique_des_Studios_Disney", "Infobox_Humoriste", "Infobox_Hydro-Québec_(historique)", "Infobox_Hymne", "Infobox_Hélicoptère", "Infobox_Hôpital", "Infobox_Hôtel", "Infobox_IVC_Telecom", "Infobox_Idéogramme", "Infobox_Indice_boursier", "Infobox_Infraction", "Infobox_Infraction_en_France", "Infobox_Infraction_en_Suisse", "Infobox_Initiative_et_référendum_suisse", "Infobox_Installation_nucléaire", "Infobox_Intercommunalité_de_France", "Infobox_Intervention", "Infobox_Inventaire_du_patrimoine_culturel_immatériel_en_France", "Infobox_Isotope", "Infobox_Isotope_RMN", "Infobox_Isthme", "Infobox_Jaguar", "Infobox_Jeu", "Infobox_Jeu_de_cartes", "Infobox_Jeu_de_données", "Infobox_Jeu_vidéo", "Infobox_Jeux_olympiques", "Infobox_Jeux_olympiques_de_la_jeunesse", "Infobox_Jeux_paralympiques", "Infobox_Joueur_d'échecs", "Infobox_Joueur_de_badminton", "Infobox_Joueur_de_baseball", "Infobox_Joueur_de_baseball2", "Infobox_Joueur_de_basket-ball", "Infobox_Joueur_de_cricket", "Infobox_Joueur_de_futsal", "Infobox_Joueur_de_go", "Infobox_Joueur_de_hockey_sur_gazon", "Infobox_Joueur_de_jeux_vidéo", "Infobox_Joueur_de_poker", "Infobox_Joueur_de_pétanque", "Infobox_Joueur_de_rink_hockey", "Infobox_Joueur_de_snooker", "Infobox_Joueur_de_sport_gaélique", "Infobox_Joueur_de_squash", "Infobox_Joueur_de_tennis", "Infobox_Joueur_de_volley-ball", "Infobox_Joueur_de_water-polo", "Infobox_Jour", "Infobox_Journaliste", "Infobox_Journées_Mondiales_de_la_Jeunesse", "Infobox_Județ_de_Roumanie", "Infobox_Judoka", "Infobox_Juridiction_christianisme", "Infobox_Kabupaten_d'Indonésie", "Infobox_Koryu_bujutsu", "Infobox_Lac", "Infobox_Langage_de_programmation", "Infobox_Langue", "Infobox_Langue_zone_d'influence", "Infobox_Langues_par_pays", "Infobox_Lavoir", "Infobox_Leader_chrétien", "Infobox_Lego", "Infobox_Licence", "Infobox_Licence_de_logiciel", "Infobox_Lieu_de_fiction", "Infobox_Lieu_de_fiction_(bande_dessinée)", "Infobox_Lieu_de_la_Terre_du_Milieu", "Infobox_Lieu_des_Simpson", "Infobox_Lieu_légendaire", "Infobox_Ligne_Maginot", "Infobox_Ligne_de_transport_en_commun", "Infobox_Ligne_ferroviaire", "Infobox_Ligne_à_haute_tension", "Infobox_Linguiste", "Infobox_Liste_de_fichiers", "Infobox_Liste_de_joueurs", "Infobox_Liste_de_récompenses", "Infobox_Livre", "Infobox_Livre_de_la_Bible", "Infobox_Livre_du_Disque-Monde", "Infobox_Localité", "Infobox_Localité_d'Algérie", "Infobox_Localité_d'Allemagne", "Infobox_Localité_d'Andorre", "Infobox_Localité_d'Autriche", "Infobox_Localité_d'Espagne", "Infobox_Localité_d'Islande", "Infobox_Localité_d'Ukraine", "Infobox_Localité_de_Belgique", "Infobox_Localité_de_Biélorussie", "Infobox_Localité_de_France", "Infobox_Localité_de_Norvège", "Infobox_Localité_de_Suisse", "Infobox_Localité_de_Suède", "Infobox_Localité_des_Pays-Bas", "Infobox_Localité_du_Burkina_Faso", "Infobox_Localité_du_Costa_Rica", "Infobox_Localité_du_Groenland", "Infobox_Localité_du_Liechtenstein", "Infobox_Localité_du_Luxembourg", "Infobox_Localité_du_Maroc", "Infobox_Logiciel", "Infobox_Logiciel_malveillant", "Infobox_Loi_Rome_antique", "Infobox_Lorraine", "Infobox_Lycée_en_France", "Infobox_Législature_autonomique_d'Espagne", "Infobox_Législature_canadienne", "Infobox_Législature_d'Espagne", "Infobox_Législature_d'Écosse", "Infobox_Législature_de_France", "Infobox_Législature_de_Grèce", "Infobox_Législature_de_l'Irlande", "Infobox_Législature_du_Luxembourg", "Infobox_Législature_du_pays_de_Galles", "Infobox_Législature_fédérale_suisse", "Infobox_Légume", "Infobox_MLB_All-Star_Game", "Infobox_MMA", "Infobox_MMA_event", "Infobox_Machines_de_l'île", "Infobox_Macintosh", "Infobox_Magistrat_Rome_Antique", "Infobox_Magnétosphère", "Infobox_Maison", "Infobox_Maison_d'édition", "Infobox_Maison_d'édition_de_livres-jeux", "Infobox_Maison_princière", "Infobox_Maladie", "Infobox_Maladie_des_plantes", "Infobox_Maladie_génétique", "Infobox_Manade", "Infobox_Manifestation", "Infobox_Mannequin", "Infobox_Manuscrit", "Infobox_Manuscrit_du_Nouveau_Testament", "Infobox_Marché", "Infobox_Marionnette", "Infobox_Marque", "Infobox_Marz_d'Arménie", "Infobox_Massacre", "Infobox_Master", "Infobox_Match_de_basket-ball", "Infobox_Match_de_football", "Infobox_Match_de_football_américain", "Infobox_Match_de_hockey_sur_glace", "Infobox_Match_de_rugby_à_XV", "Infobox_Match_de_tennis", "Infobox_Matériaux", "Infobox_Matériel_ferroviaire", "Infobox_Matériel_informatique", "Infobox_Mecha", "Infobox_Membre_de_Chambre_de_la_fédération_d'Éthiopie", "Infobox_Merveilles_du_monde", "Infobox_Mets", "Infobox_Micro-région_de_Hongrie", "Infobox_Microprocesseur", "Infobox_Microrégion_du_Brésil", "Infobox_Militant", "Infobox_Mine", "Infobox_Mine_du_Bassin_minier_du_Nord-Pas-de-Calais", "Infobox_Minéral", "Infobox_Miss", "Infobox_Missile", "Infobox_Mission_Apollo", "Infobox_Mission_diplomatique", "Infobox_Mission_ravitaillement_spatial", "Infobox_Mission_spatiale", "Infobox_Missions_ONU", "Infobox_Missions_UE", "Infobox_Moine_militaire_hospitalier", "Infobox_Mois", "Infobox_Monastère", "Infobox_Monnaie", "Infobox_Montagne", "Infobox_Montagnes_russes", "Infobox_Montre", "Infobox_Monument", "Infobox_Monument_Rome_Antique", "Infobox_Monument_de_la_Grèce_antique", "Infobox_Monument_historique_roumain", "Infobox_Moselstellung", "Infobox_Moteur", "Infobox_Moteur-fusée", "Infobox_Moteur_d'avion", "Infobox_Motocyclette", "Infobox_Mouvement_artistique", "Infobox_Mouvement_religieux", "Infobox_Municipalité_d'Islande", "Infobox_Municipalité_de_Bosnie-Herzégovine", "Infobox_Municipalité_de_Colombie", "Infobox_Municipalité_de_Finlande", "Infobox_Municipalité_de_Lituanie", "Infobox_Municipalité_de_Macédoine_du_Nord", "Infobox_Municipalité_de_Nouvelle-Zélande", "Infobox_Municipalité_de_Serbie", "Infobox_Municipalité_du_Canada", "Infobox_Municipalité_du_Venezuela", "Infobox_Municipalité_ontarienne", "Infobox_Municipalité_régionale_de_comté", "Infobox_Muscle", "Infobox_Musique_(artiste)", "Infobox_Musique_(discographie)", "Infobox_Musique_(festival)", "Infobox_Musique_(instrument)", "Infobox_Musique_(instrument_célèbre)", "Infobox_Musique_(label)", "Infobox_Musique_(récompense)", "Infobox_Musique_(studio)", "Infobox_Musique_(style)", "Infobox_Musique_(tournée)", "Infobox_Musique_(œuvre)", "Infobox_Musique_classique_(ensemble)", "Infobox_Musique_classique_(ensemble)2", "Infobox_Musique_classique_(personnalité)", "Infobox_Musique_classique_(œuvre)", "Infobox_Musée", "Infobox_Mécanisme", "Infobox_Médaille_militaire", "Infobox_Média", "Infobox_Médicament", "Infobox_Mégalithe", "Infobox_Mémorial_militaire", "Infobox_Mésorégion_du_Brésil", "Infobox_Méthode_scientifique", "Infobox_Métier", "Infobox_Métropole_de_France", "Infobox_Météorite", "Infobox_Nageur", "Infobox_Nation_aux_Deaflympics", "Infobox_Nation_aux_Jeux", "Infobox_Nation_aux_Jeux_du_Commonwealth", "Infobox_Nation_aux_Jeux_européens", "Infobox_Nation_aux_Jeux_méditerranéens", "Infobox_Nation_aux_Jeux_olympiques", "Infobox_Nation_aux_Jeux_paralympiques", "Infobox_Nation_en_compétition_continentale_de_Handball", "Infobox_Nation_en_compétition_continentale_de_football", "Infobox_Nation_à_la_Coupe_du_monde_de_football", "Infobox_Navette_spatiale", "Infobox_Navire", "Infobox_Nerf", "Infobox_Niveau_de_plongée", "Infobox_Niveau_géologique", "Infobox_Nom_coréen", "Infobox_Nom_de_famille", "Infobox_Nombre", "Infobox_Nome_de_Grèce", "Infobox_Norme_juridique", "Infobox_Notes_de_jeu_vidéo", "Infobox_Notes_de_série_de_jeux_vidéo", "Infobox_Nouvelle", "Infobox_Nuage", "Infobox_Nœud", "Infobox_Obchtina_de_Bulgarie", "Infobox_Objectif_photographique", "Infobox_Objet", "Infobox_Objet_astronomique", "Infobox_Objet_préhistorique", "Infobox_Oblast_d'Ukraine", "Infobox_Observatoire", "Infobox_Observatoire_v2", "Infobox_Obélisque", "Infobox_Occitanie", "Infobox_Oléicole", "Infobox_Opéra_(compagnie)", "Infobox_Opéra_(œuvre)", "Infobox_Opération_militaire", "Infobox_Orchestration", "Infobox_Orchidée", "Infobox_Ordre_de_chevalerie", "Infobox_Ordre_religieux", "Infobox_Organisation", "Infobox_Organisation2", "Infobox_Organisation_criminelle", "Infobox_Organisation_des_Nations_unies", "Infobox_Organisation_des_Royaumes_oubliés", "Infobox_Organisation_intergouvernementale", "Infobox_Orgue", "Infobox_Ouvrage", "Infobox_Ouvrage_d'art", "Infobox_Panchen_Lama", "Infobox_Panneau_de_signalisation", "Infobox_Papyrologue", "Infobox_Parc_de_loisirs", "Infobox_Parfum", "Infobox_Parlement", "Infobox_Paroisse_anglo-normande", "Infobox_Paroisse_catholique", "Infobox_Paroisse_d'Andorre", "Infobox_Paroisse_du_Venezuela", "Infobox_Parti_politique", "Infobox_Parti_politique_du_Québec", "Infobox_Particule", "Infobox_Partido_Argentine", "Infobox_Patineur_artistique", "Infobox_Patrimoine_culturel_immatériel_de_l'humanité", "Infobox_Patrimoine_mondial", "Infobox_Patrimoine_mondial_2", "Infobox_Pays", "Infobox_Pays_Bretagne", "Infobox_Pays_Eurovision", "Infobox_Pays_Eurovision_Asie", "Infobox_Pays_Loi_LOADDT", "Infobox_Pays_basque", "Infobox_Personnage_(Disney)", "Infobox_Personnage_(fiction)", "Infobox_Personnage_de_Black_Clover", "Infobox_Personnage_de_JoJo's_Bizarre_Adventure", "Infobox_Personnage_de_Naruto", "Infobox_Personnage_de_One_Piece", "Infobox_Personnage_des_Royaumes_oubliés", "Infobox_Personnalité_de_l'Égypte_antique", "Infobox_Personnalité_des_sciences_humaines_et_sociales", "Infobox_Personnalité_du_football_américain", "Infobox_Personnalité_du_hockey_sur_gazon", "Infobox_Personnalité_du_hockey_sur_glace", "Infobox_Personnalité_du_renseignement", "Infobox_Personnalité_militaire", "Infobox_Personnalité_politique", "Infobox_Peuple_antique", "Infobox_Phare", "Infobox_Philosophe", "Infobox_Photographie", "Infobox_Pierre_précieuse", "Infobox_Pierre_runique", "Infobox_Pilote", "Infobox_Pilote_NASCAR", "Infobox_Pilote_de_Rallye", "Infobox_Pilote_de_Vitesse_moto", "Infobox_Pilote_sur_circuit", "Infobox_Pipeline", "Infobox_Piste_cyclable", "Infobox_Piste_de_ski", "Infobox_Pièce", "Infobox_Pièce_de_théâtre", "Infobox_Plage", "Infobox_Plan_d'eau", "Infobox_Planeur", "Infobox_Planète", "Infobox_Planète_Fondation", "Infobox_Planète_fictive", "Infobox_Planète_mineure", "Infobox_Plaque_tectonique", "Infobox_Plate-forme_automobile", "Infobox_Playboy_Playmate", "Infobox_Pluie_de_météores", "Infobox_Poids_lourd", "Infobox_Point_chaud", "Infobox_Point_de_vue_panoramique", "Infobox_Police", "Infobox_Police_d'écriture", "Infobox_Politique_européenne", "Infobox_Politique_publique", "Infobox_Polytope", "Infobox_Polyèdre", "Infobox_Polyèdre_prisme", "Infobox_Pongiste", "Infobox_Pont", "Infobox_Pornographie_(film)", "Infobox_Pornographie_(personnalité)", "Infobox_Port", "Infobox_Porte_de_Paris", "Infobox_Poste_politique", "Infobox_Powiat_de_Pologne", "Infobox_Poème", "Infobox_Pratique_sportive_nationale", "Infobox_Presse_écrite", "Infobox_Producteur", "Infobox_Produits_du_terroir", "Infobox_Programme_spatial", "Infobox_Projet_urbain", "Infobox_Protocole_réseau_sur_la_couche_application", "Infobox_Protéine", "Infobox_Province_d'Angola", "Infobox_Province_d'Argentine", "Infobox_Province_d'Espagne", "Infobox_Province_d'Indonésie", "Infobox_Province_d'Irlande", "Infobox_Province_d'Italie", "Infobox_Province_de_Belgique", "Infobox_Province_de_Bolivie", "Infobox_Province_de_Chine", "Infobox_Province_de_Cuba", "Infobox_Province_de_Finlande", "Infobox_Province_de_Mongolie", "Infobox_Province_de_Suède", "Infobox_Province_de_Thaïlande", "Infobox_Province_de_Turquie", "Infobox_Province_de_Zambie", "Infobox_Province_de_la_république_démocratique_du_Congo", "Infobox_Province_des_Pays-Bas", "Infobox_Province_du_Burkina_Faso", "Infobox_Province_du_Cambodge", "Infobox_Province_du_Chili", "Infobox_Province_du_Costa_Rica", "Infobox_Province_du_Gabon", "Infobox_Province_du_Maroc", "Infobox_Province_du_Pakistan", "Infobox_Province_du_Pérou", "Infobox_Province_du_Viêt_Nam", "Infobox_Province_du_Zimbabwe", "Infobox_Province_ou_territoire_du_Canada", "Infobox_Préfecture_du_Japon", "Infobox_Prélat_catholique", "Infobox_Prénom", "Infobox_Prénom_japonais", "Infobox_Présidence", "Infobox_Présidence_du_Conseil_de_l'UE", "Infobox_Puits_de_mine", "Infobox_Pulsar", "Infobox_Pyramide_égyptienne", "Infobox_Pâte_alimentaire", "Infobox_Pédale_d'effet", "Infobox_Période_glaciaire", "Infobox_Périodique", "Infobox_Périphérie_de_Grèce", "Infobox_Périphérique_de_jeux_vidéo", "Infobox_Quartier", "Infobox_Quartier_américain", "Infobox_Quartier_canadien", "Infobox_Quartier_de_Belgique", "Infobox_Quartier_de_Buenos_Aires", "Infobox_Quartier_de_Jérusalem-Est", "Infobox_Quartier_de_Londres", "Infobox_Quartier_de_Québec", "Infobox_Rabbi", "Infobox_Race", "Infobox_Race_de_Stargate", "Infobox_Radar", "Infobox_Radical", "Infobox_Raffinerie", "Infobox_Raion_d'Azerbaïdjan", "Infobox_Raion_de_Biélorussie", "Infobox_Raion_de_Moldavie", "Infobox_Rajons_de_Lettonie", "Infobox_Rallye_automobile", "Infobox_Recensement", "Infobox_Record_sportif", "Infobox_Reculée", "Infobox_Refuge", "Infobox_Relations_UE-État_membre", "Infobox_Relations_bilatérales", "Infobox_Relief", "Infobox_Relief_terrestre", "Infobox_Religion", "Infobox_Religion_par_pays", "Infobox_Religion_v2", "Infobox_Remontée_mécanique", "Infobox_Représentation_des_minorités", "Infobox_Resort", "Infobox_Restaurant", "Infobox_Revue", "Infobox_Risque", "Infobox_Rites_par_religion", "Infobox_Rivalité_dans_le_sport", "Infobox_Rivière", "Infobox_Robe_animale", "Infobox_Roche", "Infobox_Roman_Royaumes_oubliés", "Infobox_Rose", "Infobox_Route", "Infobox_Route_européenne", "Infobox_Route_projet", "Infobox_Route_à_modules", "Infobox_Royaume_coutumier_de_Wallis-et-Futuna", "Infobox_Rue_de_Montréal", "Infobox_Rue_de_l'agglomération_de_Longueuil", "Infobox_Rugbyman", "Infobox_Rune", "Infobox_Réacteur_nucléaire_à_fusion", "Infobox_Réaction_chimique", "Infobox_Récompense", "Infobox_Récompense_sportive", "Infobox_Régate", "Infobox_Région", "Infobox_Région_d'Italie", "Infobox_Région_de_Belgique", "Infobox_Région_de_Côte_d'Ivoire", "Infobox_Région_de_France", "Infobox_Région_de_Hongrie", "Infobox_Région_de_Madagascar", "Infobox_Région_de_Slovaquie", "Infobox_Région_de_Tchéquie", "Infobox_Région_de_la_Macédoine_du_Nord", "Infobox_Région_de_la_République_du_Congo", "Infobox_Région_des_Royaumes_oubliés", "Infobox_Région_du_Brésil", "Infobox_Région_du_Burkina_Faso", "Infobox_Région_du_Cameroun", "Infobox_Région_du_Chili", "Infobox_Région_du_Danemark", "Infobox_Région_du_Ghana", "Infobox_Région_du_Guyana", "Infobox_Région_du_Haut-Karabagh", "Infobox_Région_du_Mali", "Infobox_Région_du_Maroc", "Infobox_Région_du_Pérou", "Infobox_Région_du_Québec", "Infobox_Région_du_Sénégal", "Infobox_Région_du_Tchad", "Infobox_Région_naturelle", "Infobox_Région_viticole", "Infobox_Région_électorale_pour_l'assemblée_nationale_du_pays_de_Galles", "Infobox_Rémanent_de_supernova", "Infobox_Réseau_IRC", "Infobox_Réseau_de_diffusion", "Infobox_Réseau_de_transport_en_commun", "Infobox_Réseau_hydro", "Infobox_Réseau_routier", "Infobox_Réserve_de_biosphère", "Infobox_Résolution_de_l'ONU", "Infobox_Rôle_monarchique", "Infobox_Saint", "Infobox_Saison_ATP", "Infobox_Saison_WTA", "Infobox_Saison_amateur_de_club_de_football", "Infobox_Saison_cyclonique", "Infobox_Saison_d'équipe_cycliste", "Infobox_Saison_d'équipe_de_football_américain", "Infobox_Saison_d'équipe_de_hockey_sur_glace", "Infobox_Saison_de_basket-ball", "Infobox_Saison_de_foot", "Infobox_Saison_de_football_américain", "Infobox_Saison_de_handball", "Infobox_Saison_de_hockey_sur_gazon", "Infobox_Saison_de_hockey_sur_glace", "Infobox_Saison_de_rugby", "Infobox_Saison_de_série_télévisée", "Infobox_Saison_du_Football_Canadien", "Infobox_Saison_ligue_CFL", "Infobox_Saison_par_franchise_MLB", "Infobox_Saison_sportive", "Infobox_Salle_de_spectacle", "Infobox_Salle_de_spectacle2", "Infobox_Sanctuaire_religieux", "Infobox_Satellite_naturel", "Infobox_Sauteur_à_ski", "Infobox_Savoie", "Infobox_Scientifique", "Infobox_Secrétaire_général_de_l'ONU", "Infobox_Secteur_de_Bucarest", "Infobox_Secteur_de_l'Antarctique", "Infobox_Secteur_pavé", "Infobox_Section_communale_d'Haïti", "Infobox_Seigneurie", "Infobox_Sentier", "Infobox_Signal_d'ondes_gravitationnelles", "Infobox_Signe_du_Zodiaque", "Infobox_Signe_ou_symptôme", "Infobox_Sinogramme", "Infobox_Site_archéologique", "Infobox_Site_d'essais_militaires", "Infobox_Site_d'intérêt_scientifique_particulier", "Infobox_Site_d'Égypte_antique", "Infobox_Site_web", "Infobox_Skateur_professionnel", "Infobox_Société", "Infobox_Société_d'étudiants", "Infobox_Société_secrète", "Infobox_Socket", "Infobox_Soleil", "Infobox_Solide_de_Johnson", "Infobox_Sonnet_de_Shakespeare", "Infobox_Sourate", "Infobox_Source", "Infobox_Source_de_la_mythologie_nordique", "Infobox_Spationaute", "Infobox_Spectrographe", "Infobox_Sport", "Infobox_Sport_olympique", "Infobox_Sport_par_localisation", "Infobox_Sport_paralympique", "Infobox_Sportif", "Infobox_Spot_de_surf", "Infobox_Stade", "Infobox_Standard_de_jazz", "Infobox_Star_Wars", "Infobox_Station_de_métro", "Infobox_Station_de_radio", "Infobox_Station_de_ski", "Infobox_Station_thermale", "Infobox_Structure_géologique", "Infobox_Structure_militaire", "Infobox_Structure_unité", "Infobox_Style_architectural", "Infobox_Subdivision", "Infobox_Subdivision_administrative", "Infobox_Subdivision_d'Helsinki", "Infobox_Subdivision_de_Taïwan", "Infobox_Subdivision_de_l'île_de_Man", "Infobox_Subdivision_des_Maldives", "Infobox_Subdivision_du_Burkina_Faso", "Infobox_Subdivision_du_Kenya", "Infobox_Subdivision_du_Népal", "Infobox_Sujet_fédéral_de_Russie", "Infobox_Supporters_de_club_de_football", "Infobox_Surfeur", "Infobox_Symboles_des_États-Unis", "Infobox_Syndicat_de_la_Coupe_de_l'America", "Infobox_Synthèse_annuelle_en_astronautique", "Infobox_Synthétiseur", "Infobox_Système_d'exploitation", "Infobox_Système_d'écriture", "Infobox_Système_de_fichiers", "Infobox_Système_de_positionnement_par_satellites", "Infobox_Système_planétaire", "Infobox_Système_éducatif", "Infobox_Séisme", "Infobox_Sélection_olympique", "Infobox_Série_de_jeux_vidéo", "Infobox_Série_de_livres-jeux", "Infobox_Série_mondiale", "Infobox_Série_télévisée", "Infobox_Série_télévisée_détaillée", "Infobox_Séries_de_hockey_sur_glace", "Infobox_Tableau_Grand_Chelem", "Infobox_Tapis_persan", "Infobox_Taxon", "Infobox_Technique_de_combat", "Infobox_Technique_de_fiction", "Infobox_Technologie_d'assainissement", "Infobox_Technopôle", "Infobox_Temple_bouddhiste", "Infobox_Temple_de_la_renommée", "Infobox_Temple_hindouiste", "Infobox_Temple_égyptien", "Infobox_Tennis_aux_Jeux_olympiques_d'été", "Infobox_Terrain_de_golf", "Infobox_Terril_du_Bassin_minier_du_Nord-Pas-de-Calais", "Infobox_Territoire", "Infobox_Territoire_britannique_d'outre-mer", "Infobox_Territoire_de_la_République_démocratique_du_Congo", "Infobox_Test_psychologique", "Infobox_Tibétain_chinois", "Infobox_Timbre", "Infobox_Titre_cardinalice", "Infobox_Titre_de_livre-jeu", "Infobox_Titre_de_noblesse", "Infobox_Titre_de_transport", "Infobox_Tombeau_de_l'Égypte_antique", "Infobox_Torero", "Infobox_Tournoi_de_badminton", "Infobox_Tournoi_de_golf", "Infobox_Tournoi_de_snooker", "Infobox_Tournoi_de_squash", "Infobox_Tournoi_de_tennis", "Infobox_Train_de_voyageurs_baptisé", "Infobox_Traité", "Infobox_Traité_international", "Infobox_Tramway", "Infobox_Transport_en_commun_de_Montréal", "Infobox_Transport_ferroviaire", "Infobox_Tremplin_de_saut_à_ski", "Infobox_Tribu_d'Algérie", "Infobox_Tribu_de_Nouvelle-Calédonie", "Infobox_Tribu_du_Maroc", "Infobox_Tribunal", "Infobox_Tunnel", "Infobox_Type_MBTI", "Infobox_Type_de_bateau", "Infobox_Type_de_subdivision_administrative", "Infobox_Type_de_véhicule", "Infobox_Télescope", "Infobox_Téléphone_mobile", "Infobox_Union", "Infobox_Unité", "Infobox_Unité_lithostratigraphique", "Infobox_Unité_militaire", "Infobox_Univers_de_fiction", "Infobox_Université", "Infobox_Usine", "Infobox_Utilisateur", "Infobox_V2", "Infobox_Vaccin", "Infobox_Vaisseau_de_fiction", "Infobox_Valeur_nutritionnelle", "Infobox_Vallée", "Infobox_Variété_de_pomme_de_terre", "Infobox_Veine", "Infobox_Vidéaste_web", "Infobox_Village_(wieś)_de_Pologne", "Infobox_Ville_d'Afghanistan", "Infobox_Ville_d'Afrique_du_Sud", "Infobox_Ville_d'Arabie_saoudite", "Infobox_Ville_d'Australie", "Infobox_Ville_d'Azerbaïdjan", "Infobox_Ville_d'Estonie", "Infobox_Ville_d'Haïti", "Infobox_Ville_d'Irlande", "Infobox_Ville_d'Irlande_du_Nord", "Infobox_Ville_d'Israël", "Infobox_Ville_d'Uruguay", "Infobox_Ville_d'Écosse", "Infobox_Ville_d'Égypte_antique", "Infobox_Ville_d'Éthiopie", "Infobox_Ville_de_Biélorussie", "Infobox_Ville_de_Bolivie", "Infobox_Ville_de_Bosnie-Herzégovine", "Infobox_Ville_de_Chine", "Infobox_Ville_de_Corée_du_Nord", "Infobox_Ville_de_Crimée", "Infobox_Ville_de_Croatie", "Infobox_Ville_de_Dominique", "Infobox_Ville_de_Grèce", "Infobox_Ville_de_Jordanie", "Infobox_Ville_de_Lituanie", "Infobox_Ville_de_Macédoine_du_Nord", "Infobox_Ville_de_Madagascar", "Infobox_Ville_de_Moldavie", "Infobox_Ville_de_Papouasie-Nouvelle-Guinée", "Infobox_Ville_de_Pologne", "Infobox_Ville_de_Russie", "Infobox_Ville_de_Serbie", "Infobox_Ville_de_Slovénie", "Infobox_Ville_de_Syrie", "Infobox_Ville_de_Tchéquie", "Infobox_Ville_de_Tunisie", "Infobox_Ville_de_Turquie", "Infobox_Ville_de_l'Inde", "Infobox_Ville_de_la_république_démocratique_du_Congo", "Infobox_Ville_des_Philippines", "Infobox_Ville_des_Royaumes_oubliés", "Infobox_Ville_des_États-Unis", "Infobox_Ville_du_Botswana", "Infobox_Ville_du_Brésil", "Infobox_Ville_du_Gabon", "Infobox_Ville_du_Guatemala", "Infobox_Ville_du_Guyana", "Infobox_Ville_du_Japon", "Infobox_Ville_du_Kosovo", "Infobox_Ville_du_Maroc", "Infobox_Ville_du_Monténégro", "Infobox_Ville_du_Royaume-Uni", "Infobox_Ville_du_Rwanda", "Infobox_Ville_du_Sénégal", "Infobox_Ville_du_Togo", "Infobox_Ville_du_Venezuela", "Infobox_Ville_du_Viêt_Nam", "Infobox_Ville_statut_controversé", "Infobox_VinoDOC", "Infobox_Voblast_de_Biélorussie", "Infobox_Voie_d'Aix-les-Bains", "Infobox_Voie_d'escalade", "Infobox_Voie_de_Belgique", "Infobox_Voie_de_Bucarest", "Infobox_Voie_de_Buenos_Aires", "Infobox_Voie_de_Liège", "Infobox_Voie_de_Marseille", "Infobox_Voie_de_New_York", "Infobox_Voie_de_Paris", "Infobox_Voie_de_Versailles", "Infobox_Voiture_train", "Infobox_Voivodie_de_Pologne", "Infobox_Volcan", "Infobox_Volcan2", "Infobox_Véhicule_Spatial", "Infobox_Vêtement", "Infobox_Wallonie", "Infobox_Web_TV", "Infobox_Wilaya_d'Algérie", "Infobox_Zone_INSEE", "Infobox_Zone_Insee_2", "Infobox_Zone_d'administration_locale_d'Australie", "Infobox_Zone_d'Éthiopie", "Infobox_Zone_de_gouvernement_local_du_pays_de_Galles", "Infobox_Zone_de_secours", "Infobox_Zone_thématique", "Infobox_Zoo", "Infobox_en_Lua", "Infobox_iPod", "Infobox_kata_karaté", "Infobox_manquante", "Infobox_martial_arts_tournament", "Infobox_military_conflict", "Infobox_Ère_chinoise", "Infobox_Échangeur", "Infobox_Éclipse", "Infobox_Écluse", "Infobox_École", "Infobox_École_de_Yoga", "Infobox_École_de_samba", "Infobox_Économie", "Infobox_Économie_sousdivision", "Infobox_Écorégion_d'eau_douce", "Infobox_Écorégion_marine", "Infobox_Écorégion_terrestre", "Infobox_Écrivain", "Infobox_Écurie_automobile", "Infobox_Édifice_religieux", "Infobox_Édition_de_Wikipédia", "Infobox_Édition_linguistique_de_Wikipédia", "Infobox_Église", "Infobox_Église_catholique_orientale", "Infobox_Église_orientale", "Infobox_Église_orthodoxe", "Infobox_Église_protestante", "Infobox_Égyptologue", "Infobox_Élection", "Infobox_Élection_de_Miss", "Infobox_Élus_commune", "Infobox_Élément", "Infobox_Émission_de_radio", "Infobox_Émission_de_télévision", "Infobox_Énergie_(pays)", "Infobox_Éolienne", "Infobox_Éparchie_catholique", "Infobox_Éphéméride", "Infobox_Éphéméride_Catholicisme", "Infobox_Éphéméride_Disney", "Infobox_Éphéméride_de_l'Anjou_et_de_Maine-et-Loire", "Infobox_Éphéméride_des_chemins_de_fer", "Infobox_Éphéméride_du_sport", "Infobox_Éphéméride_mois_de_l'année", "Infobox_Éphéméride_républicaine", "Infobox_Éphéméride_républicaine_6e_jour_complémentaire", "Infobox_Épice", "Infobox_Épidémie", "Infobox_Épisode_biblique", "Infobox_Épisode_de_Doctor_Who", "Infobox_Épisode_de_série_télévisée", "Infobox_Épisode_des_Simpson", "Infobox_Épreuve_d'athlétisme", "Infobox_Équipe_cycliste", "Infobox_Équipe_de_Coupe_Davis_ou_de_Fed_Cup", "Infobox_Équipe_de_cricket", "Infobox_Équipe_de_football_américain", "Infobox_Équipe_de_hockey_sur_glace", "Infobox_Équipe_de_sport_électronique", "Infobox_Équipe_du_State_of_Origin", "Infobox_Équipe_nationale_de_bandy", "Infobox_Équipe_nationale_de_baseball", "Infobox_Équipe_nationale_de_basket-ball", "Infobox_Équipe_nationale_de_beach_soccer", "Infobox_Équipe_nationale_de_football", "Infobox_Équipe_nationale_de_football_américain", "Infobox_Équipe_nationale_de_futsal", "Infobox_Équipe_nationale_de_handball", "Infobox_Équipe_nationale_de_hockey_sur_gazon", "Infobox_Équipe_nationale_de_hockey_sur_glace", "Infobox_Équipe_nationale_de_kayak-polo", "Infobox_Équipe_nationale_de_rink_hockey", "Infobox_Équipe_nationale_de_roller_in_line_hockey", "Infobox_Équipe_nationale_de_rugby_à_XIII", "Infobox_Équipe_nationale_de_rugby_à_XV", "Infobox_Équipe_nationale_de_volley-ball", "Infobox_Équipe_nationale_de_water-polo", "Infobox_Équipe_nationale_féminine_de_football", "Infobox_Équipe_nationale_sportive", "Infobox_Éruption_volcanique", "Infobox_Établissement_pénitentiaire", "Infobox_Établissement_scolaire", "Infobox_Étagement", "Infobox_Étape", "Infobox_Étape_du_Tour_d'Espagne", "Infobox_Étape_du_Tour_d'Italie", "Infobox_Étape_du_Tour_de_France", "Infobox_État_d'Allemagne", "Infobox_État_d'Autriche", "Infobox_État_d'Éthiopie", "Infobox_État_de_Malaisie", "Infobox_État_de_l'Inde", "Infobox_État_des_États-Unis", "Infobox_État_du_Brésil", "Infobox_État_du_Mexique", "Infobox_État_du_Nigeria", "Infobox_État_du_Venezuela", "Infobox_État_ou_territoire_d'Australie", "Infobox_Étendue_d'eau", "Infobox_Étoile", "Infobox_Études_supérieures", "Infobox_Événement", "Infobox_Événement_historique", "Infobox_Événement_météorologique", "Infobox_Événement_sportif", "Infobox_Île", "Infobox_à_usage_unique"
]
def frwiki_infobox():
	#infoboxlist = get_input_list()

	for infobox in fr_infobox_list:
		infname = infobox.replace('Infobox_','').replace('_', ' ')
		languageWiki = conn_fr
		template = infobox
		portalFr = None
		grupa = 'frinfobox'
		pywikibot.output('\t'+infname)

		if portalFr:
			result_json = one_project(portalFr,languageWiki)
		else:
			result_json = one_project_tpl(template,languageWiki)
		insert_into_db(grupa,infname,result_json)

	conn_ru.close()
	conn_fr.close()
	pywikibot.output('done')
#
frwiki_infobox()
