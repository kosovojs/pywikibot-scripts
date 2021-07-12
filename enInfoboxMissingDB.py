import pywikibot, re, os, time, sys, json
import toolforge
from datetime import date, datetime, timedelta, timezone
from pytz import timezone

conn = toolforge.connect('enwiki_p','analytics')
connLabs = toolforge.connect_tools('s53143__mis_lists_p')
cursor1 = connLabs.cursor()

utc_timezone = timezone("UTC")
lva_timezone = timezone("Europe/Riga")

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query):
	#query = query.encode('utf-8')
	#print(query)
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows
#
SQL_main = """select p.page_title, count(l.ll_lang) as langs,
	(select pp.pp_value from page_props pp where pp.pp_page=ll_from and pp_propname='wikibase_item') as wd
from langlinks l
join page p on p.page_id=l.ll_from
where  l.ll_from in (select tl.tl_from from templatelinks tl where tl.tl_title="{}" and tl_namespace=10 and tl.tl_from_namespace=0)
and p.page_namespace=0 and l.ll_from not in (select m.ll_from from langlinks m where m.ll_lang="lv")
group by l.ll_from
order by count(l.ll_lang) desc
limit 1000;"""

infoboxlist = [
	'Infobox_football_biography', 'Infobox_album', 'Infobox_officeholder', 'Infobox_film', 'Infobox_musical_artist',
	'Infobox_NRHP', 'Infobox_song', 'Infobox_company', 'Infobox_sportsperson', 'Infobox_single',
	'Infobox_television', 'Infobox_book', 'Infobox_French_commune', 'Infobox_station', 'Infobox_ship_begin',
	'Infobox_ship_characteristics', 'Infobox_ship_image', 'Infobox_military_person', 'Infobox_school', 'Infobox_ship_career',
	'Infobox_scientist', 'Infobox_writer', 'Infobox_UK_place', 'Infobox_baseball_biography', 'Infobox_cricketer',
	'Infobox_university', 'Infobox_mountain', 'Infobox_football_club', 'Infobox_video_game', 'Infobox_NCAA_team_season',
	'Infobox_organization', 'Infobox_radio_station', 'Infobox_road', 'Infobox_military_unit', 'Infobox_NFL_biography',
	'Infobox_building', 'Infobox_artist', 'Infobox_ice_hockey_player', 'Infobox_airport', 'Infobox_military_conflict',
	'Infobox_royalty', 'Infobox_river', 'Infobox_venue', 'Infobox_basketball_biography', 'Infobox_AFL_biography',
	'Infobox_German_location', 'Infobox_election', 'Infobox_body_of_water', 'Infobox_tennis_tournament_event', 'Infobox_Australian_place',
	'Infobox_aircraft_begin', 'Infobox_cyclist', 'Infobox_gene', 'Infobox_Korean_name', 'Infobox_football_club_season',
	'Infobox_Christian_leader', 'Infobox_aircraft_type', 'Infobox_football_league_season', 'Infobox_country_at_games', 'Infobox_rugby_biography',
	'Infobox_software', 'Infobox_church', 'Infobox_television_episode', 'Infobox_political_party', 'Infobox_Chinese',
	'Infobox_protected_area', 'Infobox_language', 'Infobox_Italian_comune', 'Infobox_swimmer', 'Infobox_college_coach',
	'Infobox_journal', 'Infobox_drug', 'Infobox_rugby_league_biography', 'Infobox_newspaper', 'Infobox_military_installation',
	'Infobox_museum', 'Infobox_government_agency', 'Infobox_tennis_tournament_year', 'Infobox_islands', 'Infobox_sports_competition_event',
	'Infobox_CFL_biography', 'Infobox_automobile', 'Infobox_tennis_biography', 'Infobox_artwork', 'Infobox_award',
	'Infobox_historic_site', 'Infobox_rockunit', 'Infobox_ethnic_group', 'Infobox_weapon', 'Infobox_magazine',
	'Infobox_character', 'Infobox_website', 'Infobox_religious_building', 'Infobox_television_channel', 'Infobox_UK_school',
	'Infobox_Olympic_event', 'Infobox_food', 'Infobox_enzyme', 'Infobox_noble', 'Infobox_medical_condition',
	'Infobox_rail_line', 'Infobox_name_module', 'Infobox_football_tournament_season', 'Infobox_television_season', 'Infobox_volleyball_biography',
	'Infobox_bridge', 'Infobox_artist_discography', 'Infobox_comics_character', 'Infobox_racehorse', 'Infobox_official_post',
	'Infobox_anatomy', 'Infobox_UK_disused_station', 'Infobox_boxer', 'Infobox_park', 'Infobox_recurring_event',
	'Infobox_given_name', 'Infobox_airline', 'Infobox_international_football_competition', 'Infobox_GAA_player', 'Infobox_martial_artist',
	'Infobox_football_match', 'Infobox_saint', 'Infobox_locomotive', 'Infobox_hospital', 'Infobox_figure_skater',
	'Infobox_broadcast', 'Infobox_NFL_season', 'Infobox_golfer', 'Infobox_dam', 'Infobox_diocese',
	'Infobox_sports_season', 'Infobox_planet', 'Infobox_record_label', 'Infobox_constituency', 'Infobox_designation_list',
	'Infobox_professional_wrestler', 'Infobox_handball_biography', 'Infobox_ship_class_overview', 'Infobox_court_case', 'Infobox_bilateral_relations',
	'Infobox_former_country', 'Infobox_ancient_site', 'Infobox_comics_creator', 'Infobox_U.S._county', 'Infobox_SCOTUS_case',
	'Infobox_manner_of_address', 'Infobox_concert', 'Infobox_civilian_attack', 'Infobox_criminal', 'Infobox_MLB_yearly',
	'Infobox_cycling_race_report', 'Infobox_Swiss_town', 'Infobox_shopping_mall', 'Infobox_game_score', 'Infobox_spaceflight',
	'Infobox_soap_character', 'Infobox_sports_league', 'Infobox_dim', 'Infobox_Russian_inhabited_locality', 'Infobox_school_district',
	'Infobox_Greek_Dimos', 'Infobox_pageant_titleholder', 'Infobox_comic_book_title', 'Infobox_gymnast', 'Infobox_service_record',
	'Infobox_Town_AT', 'Infobox_racing_driver', 'Infobox_lighthouse', 'Infobox_rugby_team', 'Infobox_power_station',
	'Infobox_architect', 'Infobox_GB_station', 'Infobox_play', 'Infobox_Chinese-language_singer_and_actor', 'Infobox_event',
	'Infobox_UN_resolution', 'Infobox_badminton_player', 'Infobox_rail_service', 'Infobox_basketball_club', 'Infobox_academic',
	'Infobox_philosopher', 'Infobox_South_African_town', 'Infobox_rail', 'Infobox_cultivar', 'Infobox_medical_condition_(new)',
	'Infobox_military_award', 'Infobox_horseraces', 'Infobox_legislature', 'Infobox_Russian_district', 'Infobox_Paralympic_event',
	'Infobox_Canada_electoral_district', 'Infobox_football_league', 'Infobox_UK_constituency', 'Infobox_publisher', 'Infobox_model',
	'Infobox_union', 'Infobox_ice_hockey_team_season', 'Infobox_New_Testament_manuscript', 'Infobox_mine', 'Infobox_train',
	'Infobox_Hollywood_cartoon', 'Infobox_short_story', 'Infobox_skier', 'Infobox_college_football_game', 'Infobox_former_subdivision',
	'Infobox_chess_biography', 'Infobox_aircraft_occurrence', 'Infobox_film_awards', 'Infobox_protein_family', 'Infobox_game',
	'Infobox_road_small', 'Infobox_bus_company', 'Infobox_UK_legislation', 'Infobox_lunar_crater_or_mare', 'Infobox_NBA_season',
	'Infobox_NCAA_football_yearly_game', 'Infobox_street', 'Infobox_Hindu_temple', 'Infobox_sports_team', 'Infobox_religious_biography',
	'Infobox_song_contest_entry', 'Infobox_comedian', 'Infobox_music_festival', 'Infobox_law_enforcement_agency', 'Infobox_surname',
	'Infobox_song_contest_national_year', 'Infobox_mineral', 'Infobox_musical', 'Infobox_Grand_Prix_race_report', 'Infobox_information_appliance',
	'Infobox_college_football_player', 'Infobox_hurricane', 'Infobox_prison', 'Infobox_Wrestling_event', 'Infobox_radio_show',
	'Infobox_national_football_team', 'Infobox_economist', 'Infobox_Site_of_Special_Scientific_Interest', 'Infobox_galaxy', 'Infobox_figure_skating_competition',
	'Infobox_mobile_phone', 'Infobox_Pro_hockey_team', 'Infobox_beauty_pageant', 'Infobox_library', 'Infobox_cricket_tournament',
	'Infobox_broadcasting_network', 'Infobox_Asian_Games_event', 'Infobox_holiday', 'Infobox_motorcycle_rider', 'Infobox_football_tournament',
	'Infobox_Bishop_styles', 'Infobox_hockey_team', 'Infobox_glacier', 'Infobox_Australian_Electorate', 'Infobox_racing_driver_series_section',
	'Infobox_Pan_American_Games_event', 'Infobox_musical_composition', 'Infobox_games', 'Infobox_rail_standard_gauge', 'Infobox_NASCAR_driver',
	'Infobox_mountain_pass', 'Infobox_family', 'Infobox_motorcycle', 'Infobox_route_diagram', 'Infobox_restaurant',
	'Infobox_language_family', 'Infobox_Israel_village', 'Infobox_city_Japan', 'Infobox_film_festival', 'Infobox_waterfall',
	'Infobox_animal_breed', 'Infobox_GAA_club', 'Infobox_zoo', 'Infobox_settlement_(Albanian)', 'Infobox_Municipality_BR',
	'Infobox_brand', 'Infobox_Athletics_Championships', 'Infobox_sport_governing_body', 'Infobox_legislation', 'Infobox_public_transit',
	'Infobox_beverage', 'Infobox_aircraft_engine', 'Infobox_World_Heritage_Site', 'Infobox_Parish_PT', 'Infobox_tennis_tournament',
	'Infobox_government_cabinet', 'Infobox_cycling_race', 'Infobox_NCAA_Basketball_Conference_Tournament', 'Infobox_cemetery', 'Infobox_music_genre',
	'Infobox_rfam', 'Infobox_opera', 'Infobox_speed_skater', 'Infobox_WorldScouting', 'Infobox_sports_rivalry',
	'Infobox_sailor', 'Infobox_member_of_the_Knesset', 'Infobox_Minor_League_Baseball', 'Infobox_MMA_event', 'Infobox_hiking_trail',
	'Infobox_cricket_ground', 'Infobox_horseracing_personality', 'Infobox_NASCAR_race_report', 'Infobox_individual_golf_tournament', 'Infobox_engineering_career',
	'Infobox_Christian_denomination', 'Infobox_earthquake', 'Infobox_protein', 'Infobox_racing_car', 'Infobox_F1_driver',
	'Infobox_medical_intervention', 'Infobox_FIBA_tourney', 'Infobox_golf_tournament', 'Infobox_OS', 'Infobox_civil_conflict',
	'Infobox_national_basketball_team', 'Infobox_curler', 'Infobox_school_athletics', 'Infobox_U.S._legislation', 'Infobox_book_series',
	'Infobox_rugby_union_season', 'Infobox_French_canton', 'Infobox_individual_snooker_tournament', 'Infobox_curling_competition', 'Infobox_monument',
	'Infobox_London_station', 'Infobox_cricket_team', 'Infobox_engineer', 'Infobox_NCAA_Tournament_yearly', 'Infobox_tournament',
	'Infobox_treaty', 'Infobox_roller_coaster', 'Infobox_medical_details', 'Infobox_pro_wrestling_championship', 'Infobox_historic_subdivision',
	'Infobox_amusement_park', 'Infobox_monastery', 'Infobox_speedway_rider', 'Infobox_international_hockey_competition', 'Infobox_coat_of_arms_wide',
	'Infobox_football_official', 'Infobox_Cardinal_styles', 'Infobox_war_faction', 'Infobox_college_basketball_team', 'Infobox_video_game_series',
	'Infobox_reality_talent_competition', 'Infobox_flag', 'Infobox_camera', 'Infobox_instrument', 'Infobox_rugby_league_club',
	'Infobox_darts_player', 'Infobox_FIVB_tournament', 'Infobox_diplomatic_mission', 'Infobox_Australian_road', 'Infobox_poker_player',
	'Infobox_golf_facility', 'Infobox_medical_person', 'Infobox_motorsport_venue', 'Infobox_cycling_team', 'Infobox_oil_field',
	'Infobox_tunnel', 'Infobox_New_York_City_Subway_station', 'Infobox_ski_area', 'Infobox_institute', 'Infobox_command_structure',
	'Infobox_sailboat_specifications', 'Infobox_Malaysia_electoral_district', 'Infobox_astronaut', 'Infobox_country', 'Infobox_coat_of_arms',
	'Infobox_Latter_Day_Saint_biography', 'Infobox_deity', 'Infobox_port', 'Infobox_chef', 'Infobox_Vidhan_Sabha_constituency',
	'Infobox_sport_overview', 'Infobox_cricket_tour', 'Infobox_baseball_team', 'Infobox_Simpsons_season_episode_list', 'Infobox_Simpsons_episode',
	'Infobox_handball_club', 'Infobox_clergy', 'Infobox_dog_breed', 'Infobox_culinary_career', 'Infobox_athletics_race',
	'Infobox_Belgium_Municipality', 'Infobox_programming_language', 'Infobox_comic_strip', 'Infobox_cave', 'Infobox_attraction',
	'Infobox_rugby_football_league_season', 'Infobox_Grand_Prix_motorcycle_race_report', 'Infobox_Australian_football_club', 'Infobox_presenter', 'Infobox_table_tennis_player',
	'Infobox_observatory', 'Infobox_solar_eclipse', 'Infobox_file_format', 'Infobox_alpine_ski_racer', 'Infobox_brain',
	'Infobox_legislative_term', 'Infobox_storm', 'Infobox_cross_country_championships', 'Infobox_anthem', 'Infobox_Australian_rules_football_season',
	'Infobox_crater_data', 'Infobox_nutritional_value', 'Infobox_law_firm', 'Infobox_rail_accident', 'Infobox_firearm_cartridge',
	'Infobox_snooker_player', 'Infobox_comics_organization', 'Infobox_volleyball_club', 'Infobox_engine', 'Infobox_tropical_cyclone_season',
	'Infobox_graphic_novel', 'Infobox_wine_region', 'Infobox_tropical_cyclone_small', 'Infobox_Muslim_leader', 'Infobox_artifact',
	'Infobox_football_country_season', 'Infobox_military_memorial', 'Infobox_video_game_character', 'Infobox_field_hockey', 'Infobox_international_handball_competition',
	'Infobox_audio_drama', 'Infobox_criminal_organization','Infobox_adult_biography'
]

def utc_to_local(utc_dt):
	return utc_timezone.localize(utc_dt).astimezone(lva_timezone)
#

infoboxlist = infoboxlist[::-1]

sql_insert = 'UPDATE `entries` SET jsondata=%s, last_upd=%s where group_name=%s and name=%s'
#'INSERT INTO `entries` (`name`, `group_name`, `jsondata`,`last_upd`) VALUES (%s, %s, %s, %s)'

def encode_all_items(row):
	return [encode_if_necessary(f) for f in row]

def main():
	for infobox in infoboxlist:
		pywikibot.output('\t'+infobox)
		sys.stdout.flush()
		begin = time.time()
		#result_json = []
		query_res = run_query(SQL_main.format(infobox))

		end = time.time()
		timelen = end-begin
		if timelen>30:
			pywikibot.output('{}'.format(timelen))

		result_json = [encode_all_items(f) for f in query_res]
		curr_time = utc_to_local(datetime.utcnow())
		dateforq1 = "{0:%Y%m%d%H%M%S}".format(curr_time)
		#print(dateforq1)

		#put_db(infobox,result_json,dateforq1)
		cursor1.execute(sql_insert, (str(json.dumps(result_json)), dateforq1, 'eninfobox', infobox.replace('Infobox_','').replace('_',' ')))

		connLabs.commit()
	connLabs.close()
	conn.close()
	pywikibot.output('done')

#
main()
