import pywikibot, re, requests, os, toolforge


#os.chdir(r'projects/lv')

site = pywikibot.Site("lv", "wikipedia")

res = {
    "batchcomplete": "",
    "query": {
        "namespaces": {
            "-2": {
                "id": -2,
                "case": "first-letter",
                "canonical": "Media",
                "*": "Media"
            },
            "-1": {
                "id": -1,
                "case": "first-letter",
                "canonical": "Special",
                "*": "Special"
            },
            "0": {
                "id": 0,
                "case": "first-letter",
                "content": "",
                "*": ""
            },
            "1": {
                "id": 1,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Talk",
                "*": "Diskusija"
            },
            "2": {
                "id": 2,
                "case": "first-letter",
                "subpages": "",
                "canonical": "User",
                "*": "Dal\u012bbnieks"
            },
            "3": {
                "id": 3,
                "case": "first-letter",
                "subpages": "",
                "canonical": "User talk",
                "*": "Dal\u012bbnieka diskusija"
            },
            "4": {
                "id": 4,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Project",
                "*": "Vikip\u0113dija"
            },
            "5": {
                "id": 5,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Project talk",
                "*": "Vikip\u0113dijas diskusija"
            },
            "6": {
                "id": 6,
                "case": "first-letter",
                "canonical": "File",
                "*": "Att\u0113ls"
            },
            "7": {
                "id": 7,
                "case": "first-letter",
                "subpages": "",
                "canonical": "File talk",
                "*": "Att\u0113la diskusija"
            },
            "8": {
                "id": 8,
                "case": "first-letter",
                "subpages": "",
                "canonical": "MediaWiki",
                "*": "MediaWiki"
            },
            "9": {
                "id": 9,
                "case": "first-letter",
                "subpages": "",
                "canonical": "MediaWiki talk",
                "*": "MediaWiki diskusija"
            },
            "10": {
                "id": 10,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Template",
                "*": "Veidne"
            },
            "11": {
                "id": 11,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Template talk",
                "*": "Veidnes diskusija"
            },
            "12": {
                "id": 12,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Help",
                "*": "Pal\u012bdz\u012bba"
            },
            "13": {
                "id": 13,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Help talk",
                "*": "Pal\u012bdz\u012bbas diskusija"
            },
            "14": {
                "id": 14,
                "case": "first-letter",
                "canonical": "Category",
                "*": "Kategorija"
            },
            "15": {
                "id": 15,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Category talk",
                "*": "Kategorijas diskusija"
            },
            "100": {
                "id": 100,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Port\u0101ls",
                "*": "Port\u0101ls"
            },
            "101": {
                "id": 101,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Port\u0101la diskusija",
                "*": "Port\u0101la diskusija"
            },
            "102": {
                "id": 102,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Vikiprojekts",
                "*": "Vikiprojekts"
            },
            "103": {
                "id": 103,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Vikiprojekta diskusija",
                "*": "Vikiprojekta diskusija"
            },
            "446": {
                "id": 446,
                "case": "first-letter",
                "canonical": "Education Program",
                "*": "Izgl\u012bt\u012bbas programma"
            },
            "447": {
                "id": 447,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Education Program talk",
                "*": "Izgl\u012bt\u012bbas programmas diskusija"
            },
            "828": {
                "id": 828,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Module",
                "*": "Modulis"
            },
            "829": {
                "id": 829,
                "case": "first-letter",
                "subpages": "",
                "canonical": "Module talk",
                "*": "Modu\u013ca diskusija"
            },
            "2300": {
                "id": 2300,
                "case": "first-letter",
                "canonical": "Gadget",
                "*": "Gadget"
            },
            "2301": {
                "id": 2301,
                "case": "first-letter",
                "canonical": "Gadget talk",
                "*": "Gadget talk"
            },
            "2302": {
                "id": 2302,
                "case": "case-sensitive",
                "canonical": "Gadget definition",
                "defaultcontentmodel": "GadgetDefinition",
                "*": "Gadget definition"
            },
            "2303": {
                "id": 2303,
                "case": "case-sensitive",
                "canonical": "Gadget definition talk",
                "*": "Gadget definition talk"
            },
            "2600": {
                "id": 2600,
                "case": "first-letter",
                "canonical": "Topic",
                "defaultcontentmodel": "flow-board",
                "*": "T\u0113ma"
            }
        },
        "namespacealiases": [
            {
                "id": 2,
                "*": "Dal\u012bbniece"
            },
            {
                "id": 2,
                "*": "Lietot\u0101js"
            },
            {
                "id": 3,
                "*": "Dal\u012bbnieces diskusija"
            },
            {
                "id": 3,
                "*": "Lietot\u0101ja diskusija"
            },
            {
                "id": 4,
                "*": "VP"
            },
            {
                "id": 4,
                "*": "WP"
            },
            {
                "id": 4,
                "*": "Wikipedia"
            },
            {
                "id": 6,
                "*": "Image"
            },
            {
                "id": 7,
                "*": "Image talk"
            }
        ]
    }
}

pageviewdata = {
	"items":[{"project":"en.wikipedia","access":"all-access","year":"2015","month":"10","day":"10","articles":[{"article":"Main_Page","views":18793503,"rank":1},{"article":"Special:Search","views":2629537,"rank":2},{"article":"Carlos_Hathcock","views":291358,"rank":3},{"article":"Template:GeoTemplate","views":203864,"rank":4},{"article":"Special:Book","views":158821,"rank":5},{"article":"UEFA_Euro_2016_qualifying","views":143704,"rank":6},{"article":"Web_scraping","views":115672,"rank":7},{"article":"The_Martian_(film)","views":112274,"rank":8},{"article":"Special:RecentChanges","views":106280,"rank":9},{"article":"History_of_the_M1_Abrams","views":105935,"rank":10},{"article":"American_Horror_Story:_Hotel","views":104214,"rank":11},{"article":"Dulce_María","views":98801,"rank":12},{"article":"Dr._Seuss","views":98051,"rank":13},{"article":"Pablo_Escobar","views":89626,"rank":14},{"article":"Randy_Quaid","views":80164,"rank":15},{"article":"Deaths_in_2015","views":77362,"rank":16},{"article":"2015_Rugby_World_Cup","views":74384,"rank":17},{"article":"Special:Watchlist","views":66767,"rank":18},{"article":"Philippe_Petit","views":65176,"rank":19},{"article":"Paul_Bogle","views":63044,"rank":20},{"article":"List_of_Bollywood_films_of_2015","views":62308,"rank":21},{"article":"American_Horror_Story","views":61542,"rank":22},{"article":"Pan_(2015_film)","views":60484,"rank":23},{"article":"Chikki_Panday","views":60156,"rank":24},{"article":"American_Horror_Story:_Freak_Show","views":59919,"rank":25},{"article":"Spider_web","views":58934,"rank":26},{"article":"The_Walk_(2015_film)","views":57926,"rank":27},{"article":"Jürgen_Klopp","views":56507,"rank":28},{"article":"File:Evander_Holyfield_LA_2011.jpg","views":55740,"rank":29},{"article":"Whitey_Bulger","views":54887,"rank":30},{"article":"Lyme_disease","views":54826,"rank":31},{"article":"Sunil_Deodhar","views":54547,"rank":32},{"article":"Chris_Kyle","views":54051,"rank":33},{"article":"Jacob_deGrom","views":53584,"rank":34},{"article":"Shia_LaBeouf","views":53051,"rank":35},{"article":"2008_Noida_double_murder_case","views":52684,"rank":36},{"article":"Rudrama_Devi","views":52386,"rank":37},{"article":"Steve_Jobs","views":52348,"rank":38},{"article":"Rudhramadevi_(film)","views":51735,"rank":39},{"article":"The_Walking_Dead_(TV_series)","views":51675,"rank":40},{"article":"Special:MobileMenu","views":49712,"rank":41},{"article":"Cigarette_filter","views":49174,"rank":42},{"article":"UEFA_Euro_2016","views":48073,"rank":43},{"article":"User:GoogleAnalitycsRoman/google-api","views":47464,"rank":44},{"article":"Special:WhatLinksHere/File:WikiThanks.png","views":46905,"rank":45},{"article":"America's_Next_Top_Model_(cycle_22)","views":45949,"rank":46},{"article":"Crimson_Peak","views":45139,"rank":47},{"article":"Soviet_Union","views":44139,"rank":48},{"article":"Facebook","views":43086,"rank":49},{"article":"Schism_(song)","views":42783,"rank":50},{"article":"Ddd","views":42584,"rank":51},{"article":"Troy_Carter_(music_industry)","views":42319,"rank":52},{"article":"Special:CiteThisPage","views":42289,"rank":53},{"article":"Singh_Is_Bliing","views":42175,"rank":54},{"article":"Star_Wars_Battlefront_(2015_video_game)","views":42122,"rank":55},{"article":"Knock_Knock_(2015_film)","views":41834,"rank":56},{"article":"Jazbaa","views":41824,"rank":57},{"article":"The_Documentary_2","views":41800,"rank":58},{"article":"The_Flash_(2014_TV_series)","views":40697,"rank":59},{"article":"Jim_Diamond_(singer)","views":39931,"rank":60},{"article":"Mary,_Queen_of_Scots","views":39703,"rank":61},{"article":"Million_Man_March","views":39512,"rank":62},{"article":"Sicario_(2015_film)","views":38819,"rank":63},{"article":"Stephen_Hawking","views":37304,"rank":64},{"article":"United_States","views":37005,"rank":65},{"article":"Google","views":36704,"rank":66},{"article":"List_of_people_who_disappeared_mysteriously","views":36662,"rank":67},{"article":"Scream_Queens_(2015_TV_series)","views":36467,"rank":68},{"article":"Prem_Ratan_Dhan_Payo","views":36131,"rank":69},{"article":"The_Walking_Dead_(season_6)","views":35996,"rank":70},{"article":"Fear_the_Walking_Dead","views":35868,"rank":71},{"article":"Sachin_Tendulkar","views":34980,"rank":72},{"article":"Dwayne_Johnson","views":34569,"rank":73},{"article":"Quantico_(TV_series)","views":34110,"rank":74},{"article":"Geoffrey_Howe","views":33640,"rank":75},{"article":"Selena_Gomez","views":33640,"rank":75},{"article":"Jim_Carrey","views":33315,"rank":77},{"article":"Avengers:_Age_of_Ultron","views":33264,"rank":78},{"article":"Revival_(Selena_Gomez_album)","views":33194,"rank":79},{"article":"Flash_(Jay_Garrick)","views":33140,"rank":80},{"article":"Puli_(2015_film)","views":32426,"rank":81},{"article":"Gotham_(TV_series)","views":32390,"rank":82},{"article":"Islamic_State_of_Iraq_and_the_Levant","views":32038,"rank":83},{"article":"Amy_Jackson","views":31830,"rank":84},{"article":"2015_in_film","views":31615,"rank":85},{"article":"Heroes_Reborn_(miniseries)","views":31224,"rank":86},{"article":"India","views":31169,"rank":87},{"article":"Portal:Current_events","views":31055,"rank":88},{"article":"Black_Mass_(film)","views":30984,"rank":89},{"article":"Arrow_(TV_series)","views":30937,"rank":90},{"article":"Narcos","views":30892,"rank":91},{"article":"Cosmetics_in_Ancient_Rome","views":30804,"rank":92},{"article":"Star_Wars","views":30278,"rank":93},{"article":"Everest_(2015_film)","views":30066,"rank":94},{"article":"Ben_Carson","views":29884,"rank":95},{"article":"Red_River_Showdown","views":29746,"rank":96},{"article":"Cicada_3301","views":29489,"rank":97},{"article":"Michel_Foucault","views":29388,"rank":98},{"article":"Halloween","views":29313,"rank":99},{"article":"List_of_The_Flash_(2014_TV_series)_episodes","views":29060,"rank":100},{"article":"Interstellar_(film)","views":28839,"rank":101},{"article":"Spectre_(2015_film)","views":28627,"rank":102},{"article":"Talvar_(film)","views":28425,"rank":103},{"article":"Trans-Pacific_Partnership","views":28401,"rank":104},{"article":"How_to_Get_Away_with_Murder","views":28278,"rank":105},{"article":"List_of_Steven_Universe_episodes","views":28028,"rank":106},{"article":"Baahubali:_The_Beginning","views":27890,"rank":107},{"article":"Hell_in_a_Cell_(2015)","views":27828,"rank":108},{"article":"List_of_Arrow_episodes","views":27808,"rank":109},{"article":"Matt_Damon","views":27795,"rank":110},{"article":"Star_Wars:_The_Force_Awakens","views":27517,"rank":111},{"article":"Uniform_resource_locator","views":27217,"rank":112},{"article":"List_of_The_Wanted_members","views":27087,"rank":113},{"article":"Keanu_Reeves","views":27072,"rank":114},{"article":"Donald_Trump","views":27001,"rank":115},{"article":"Manorama_(Tamil_actress)","views":26829,"rank":116},{"article":"Charlie_Strong","views":26514,"rank":117},{"article":"John_Lennon","views":26458,"rank":118},{"article":"Hail,_Caesar!","views":26411,"rank":119},{"article":"Renee_Ellmers","views":26404,"rank":120},{"article":"Mad_Max:_Fury_Road","views":26349,"rank":121},{"article":"Help:IPA_for_English","views":26038,"rank":122},{"article":"The_Weeknd","views":25980,"rank":123},{"article":"Manoj_Bhargava","views":25957,"rank":124},{"article":"Dennis_Quaid","views":25566,"rank":125},{"article":"Syrian_Civil_War","views":25493,"rank":126},{"article":"Ronda_Rousey","views":25459,"rank":127},{"article":"Phantom_time_hypothesis","views":25332,"rank":128},{"article":"Raven-Symoné","views":25294,"rank":129},{"article":"2015_Ankara_bombings","views":25282,"rank":130},{"article":"Gigi_Hadid","views":25261,"rank":131},{"article":"October_10","views":25260,"rank":132},{"article":"Causal_loop","views":25212,"rank":133},{"article":"Rugby_World_Cup","views":25203,"rank":134},{"article":"List_of_The_Walking_Dead_episodes","views":25088,"rank":135},{"article":"Matt_Bomer","views":25055,"rank":136},{"article":"Justin_Bieber","views":25012,"rank":137},{"article":"Samoa","views":24799,"rank":138},{"article":"Turkey","views":24699,"rank":139},{"article":"Poon_Lim","views":24634,"rank":140},{"article":"Barack_Obama","views":24590,"rank":141},{"article":"Stuart_Tomlinson","views":24365,"rank":142},{"article":"Ted_Hughes","views":23906,"rank":143},{"article":"Special:MobileOptions","views":23902,"rank":144},{"article":"YouTube","views":23900,"rank":145},{"article":"Fetty_Wap","views":23888,"rank":146},{"article":"Fargo_(TV_series)","views":23869,"rank":147},{"article":"Harry_Potter","views":23830,"rank":148},{"article":"Michael_Fassbender","views":23679,"rank":149},{"article":"Presidents_Cup","views":23643,"rank":150},{"article":"Mia_Khalifa","views":23601,"rank":151},{"article":"Taylor_Swift","views":23551,"rank":152},{"article":"Sunny_Leone","views":23466,"rank":153},{"article":"Jessica_Lange","views":23438,"rank":154},{"article":"List_of_World_Series_champions","views":23273,"rank":155},{"article":"Johnny_Depp","views":23171,"rank":156},{"article":"Evan_Peters","views":22864,"rank":157},{"article":"Wikipedia","views":22861,"rank":158},{"article":"Eazy-E","views":22847,"rank":159},{"article":"A._P._J._Abdul_Kalam","views":22815,"rank":160},{"article":"Jessica_Jones","views":22797,"rank":161},{"article":"Bernie_Sanders","views":22581,"rank":162},{"article":"Dylan_Larkin","views":22580,"rank":163},{"article":"List_of_Presidents_of_the_United_States","views":22574,"rank":164},{"article":"Christopher_Columbus","views":22540,"rank":165},{"article":"List_of_Naruto:_Shippuden_episodes","views":22517,"rank":166},{"article":"List_of_Victorious_episodes","views":22472,"rank":167},{"article":"Carey_Mulligan","views":22347,"rank":168},{"article":"Jurassic_World","views":22306,"rank":169},{"article":"Priyanka_Chopra","views":22246,"rank":170},{"article":"United_Kingdom","views":22228,"rank":171},{"article":"Michael_Jackson","views":22056,"rank":172},{"article":"Terrell_Owens","views":22026,"rank":173},{"article":"ABCD_2","views":22000,"rank":174},{"article":"Elon_Musk","views":21961,"rank":175},{"article":"Reign_(TV_series)","views":21843,"rank":176},{"article":"Jamie_Dornan","views":21748,"rank":177},{"article":"North_Korea","views":21665,"rank":178},{"article":"Game_of_Thrones","views":21393,"rank":179},{"article":"Special:WhatLinksHere","views":21391,"rank":180},{"article":"IZombie_(TV_series)","views":21386,"rank":181},{"article":"Empire_(2015_TV_series)","views":21347,"rank":182},{"article":"UEFA_Euro_2016_qualifying_Group_A","views":21155,"rank":183},{"article":"The_Visit_(2015_film)","views":21119,"rank":184},{"article":"Rekha","views":20898,"rank":185},{"article":"Tom_Hardy","views":20881,"rank":186},{"article":"Dr._Dre","views":20876,"rank":187},{"article":"IPTV","views":20849,"rank":188},{"article":"Eminem","views":20681,"rank":189},{"article":"Chicago_Cubs","views":20653,"rank":190},{"article":"World_War_II","views":20644,"rank":191},{"article":"John_Cena","views":20643,"rank":192},{"article":"Adolf_Hitler","views":20643,"rank":192},{"article":"Cristiano_Ronaldo","views":20496,"rank":194},{"article":"Original_Night_Stalker","views":20493,"rank":195},{"article":"The_Walking_Dead_(season_5)","views":20468,"rank":196},{"article":"Georgia_May_Foote","views":20299,"rank":197},{"article":"Doctor_Who_(series_9)","views":20211,"rank":198},{"article":"Malala_Yousafzai","views":20157,"rank":199},{"article":"List_of_unusual_deaths","views":19959,"rank":200},{"article":"Svetlana_Alexievich","views":19925,"rank":201},{"article":"Lionel_Messi","views":19883,"rank":202},{"article":"Clayton_Kershaw","views":19862,"rank":203},{"article":"Undateable","views":19827,"rank":204},{"article":"Tom_Cruise","views":19748,"rank":205},{"article":"Lea_Salonga","views":19656,"rank":206},{"article":"Jaywalking","views":19573,"rank":207},{"article":"Caitlyn_Jenner","views":19474,"rank":208},{"article":"Jackie_Robinson","views":19462,"rank":209},{"article":"Columbus_Day","views":19460,"rank":210},{"article":"Jeremy_Vine","views":19437,"rank":211},{"article":"Francis_II_of_France","views":19352,"rank":212},{"article":"Captain_America:_Civil_War","views":19346,"rank":213},{"article":"Ham_(son_of_Noah)","views":19343,"rank":214},{"article":"Mahatma_Gandhi","views":19338,"rank":215},{"article":"The_Martian_(Weir_novel)","views":19319,"rank":216},{"article":"List_of_unexplained_sounds","views":19244,"rank":217},{"article":"Emma_Roberts","views":19241,"rank":218},{"article":"List_of_Running_Man_episodes","views":19230,"rank":219},{"article":"Kim_Kardashian","views":19224,"rank":220},{"article":"Nicole_Kidman","views":19204,"rank":221},{"article":"Russian_military_intervention_in_the_Syrian_Civil_War","views":19200,"rank":222},{"article":"Cara_Delevingne","views":19143,"rank":223},{"article":"Vladimir_Putin","views":19049,"rank":224},{"article":"Wes_Bentley","views":19043,"rank":225},{"article":"Ravindra_Jain","views":19031,"rank":226},{"article":"List_of_South_Park_episodes","views":19008,"rank":227},{"article":"Katherine_Parkinson","views":18973,"rank":228},{"article":"Drake_(rapper)","views":18932,"rank":229},{"article":"The_Game_(rapper)","views":18904,"rank":230},{"article":"Wiki","views":18866,"rank":231},{"article":"Unbroken_(film)","views":18810,"rank":232},{"article":"Total_Drama_Presents:_The_Ridonculous_Race","views":18798,"rank":233},{"article":"Hotel_Transylvania_2","views":18798,"rank":233},{"article":"Robert_De_Niro","views":18785,"rank":235},{"article":"Russia","views":18780,"rank":236},{"article":"The_Vampire_Diaries_(season_7)","views":18733,"rank":237},{"article":"KickassTorrents","views":18713,"rank":238},{"article":"Dupont_de_Ligonnès_murders_and_disappearance","views":18711,"rank":239},{"article":"Strictly_Come_Dancing_(series_13)","views":18681,"rank":240},{"article":"List_of_Girl_Meets_World_episodes","views":18604,"rank":241},{"article":"The_Big_Bang_Theory","views":18524,"rank":242},{"article":"Strictly_Come_Dancing","views":18515,"rank":243},{"article":"Opinion_polling_in_the_Canadian_federal_election,_2015","views":18475,"rank":244},{"article":"World_War_I","views":18471,"rank":245},{"article":"Batman:_The_Killing_Joke","views":18465,"rank":246},{"article":"Ken_Jeong","views":18368,"rank":247},{"article":"Lady_Gaga","views":18334,"rank":248},{"article":"Kis_Kisko_Pyaar_Karoon","views":18261,"rank":249},{"article":"Doctor_Who","views":18255,"rank":250},{"article":"Amy_Winehouse","views":18249,"rank":251},{"article":"Rick_and_Morty","views":18200,"rank":252},{"article":"Once_Upon_a_Time_(TV_series)","views":18169,"rank":253},{"article":"Robin_Williams","views":18134,"rank":254},{"article":"Heath_Ledger","views":18121,"rank":255},{"article":"Mr._Robot_(TV_series)","views":18115,"rank":256},{"article":"Louis_Zamperini","views":18065,"rank":257},{"article":"Comparison_of_application_servers","views":18033,"rank":258},{"article":"Vince_Papale","views":18012,"rank":259},{"article":"Internet_Movie_Database","views":17935,"rank":260},{"article":"Jessica_Chastain","views":17913,"rank":261},{"article":"Bill_Cosby","views":17888,"rank":262},{"article":"Steve_Jobs_(2015_film)","views":17883,"rank":263},{"article":"Anita_Rani","views":17852,"rank":264},{"article":"Debits_and_credits","views":17851,"rank":265},{"article":"Invisible_Sister","views":17848,"rank":266},{"article":"Tunisian_National_Dialogue_Quartet","views":17846,"rank":267},{"article":"Franklin_D._Roosevelt","views":17799,"rank":268},{"article":"Scarlett_Johansson","views":17714,"rank":269},{"article":"Salman_Khan","views":17713,"rank":270},{"article":"List_of_Doctor_Who_serials","views":17709,"rank":271},{"article":"Bajrangi_Bhaijaan","views":17700,"rank":272},{"article":"Kray_twins","views":17678,"rank":273},{"article":"Pirates_of_the_Caribbean_(film_series)","views":17646,"rank":274},{"article":"Maze_Runner:_The_Scorch_Trials","views":17627,"rank":275},{"article":"American_Horror_Story:_Murder_House","views":17591,"rank":276},{"article":"Katie_Derham","views":17553,"rank":277},{"article":"The_Leftovers_(TV_series)","views":17541,"rank":278},{"article":"Inside_Out_(2015_film)","views":17521,"rank":279},{"article":"Canada","views":17521,"rank":279},{"article":"Ice_Cube","views":17474,"rank":281},{"article":"File:Washington_Street_(Marquette,_Michigan).jpg","views":17467,"rank":282},{"article":"Jared_Leto","views":17415,"rank":283},{"article":"Kirsty_Gallacher","views":17390,"rank":284},{"article":"Tupac_Shakur","views":17383,"rank":285},{"article":"Lupus_erythematosus","views":17195,"rank":286},{"article":"Ronald_Reagan","views":17191,"rank":287},{"article":"List_of_most_viewed_YouTube_videos","views":17177,"rank":288},{"article":"Louis_Farrakhan","views":17168,"rank":289},{"article":"UEFA_Euro_2016_qualifying_Group_B","views":17120,"rank":290},{"article":"List_of_Marvel_Cinematic_Universe_films","views":17116,"rank":291},{"article":"Yolanda_Foster","views":17106,"rank":292},{"article":"Matthew_McConaughey","views":17101,"rank":293},{"article":"John_Goodman","views":17080,"rank":294},{"article":"Nick_Easter","views":17054,"rank":295},{"article":"Straight_Outta_Compton_(2015_film)","views":17025,"rank":296},{"article":"Pixels_(2015_film)","views":17019,"rank":297},{"article":"The_Vampire_Diaries","views":17013,"rank":298},{"article":"Elizabeth_II","views":17007,"rank":299},{"article":"Australia","views":16967,"rank":300},{"article":"Dallas_Buyers_Club","views":16959,"rank":301},{"article":"The_Blacklist_(TV_series)","views":16869,"rank":302},{"article":"Ferris_Bueller's_Day_Off","views":16866,"rank":303},{"article":"Tommy_Pham","views":16853,"rank":304},{"article":"List_of_Rick_and_Morty_episodes","views":16760,"rank":305},{"article":"The_Intern_(2015_film)","views":16757,"rank":306},{"article":"Post-mortem_photography","views":16751,"rank":307},{"article":"Jyoti_Amge","views":16750,"rank":308},{"article":"Mount_Everest","views":16685,"rank":309},{"article":"Bridge_of_Spies_(film)","views":16684,"rank":310},{"article":"Carlotta_(performer)","views":16674,"rank":311},{"article":"Albert_Einstein","views":16664,"rank":312},{"article":"Demi_Lovato","views":16642,"rank":313},{"article":"O._J._Simpson","views":16618,"rank":314},{"article":"Liverpool_F.C.","views":16565,"rank":315},{"article":"Freedom_Caucus","views":16564,"rank":316},{"article":"Elizabeth_I_of_England","views":16493,"rank":317},{"article":"Homeland_(TV_series)","views":16476,"rank":318},{"article":"Zoom_(comics)","views":16405,"rank":319},{"article":"San_Andreas_(film)","views":16389,"rank":320},{"article":"Paul_Ryan","views":16385,"rank":321},{"article":"Speaker_of_the_United_States_House_of_Representatives","views":16328,"rank":322},{"article":"Ankara","views":16321,"rank":323},{"article":"Doctor_Foster_(TV_series)","views":16290,"rank":324},{"article":"Lisa_Brennan-Jobs","views":16287,"rank":325},{"article":"Girl_Meets_World","views":16274,"rank":326},{"article":"N.W.A","views":16263,"rank":327},{"article":"Mark_Wahlberg","views":16261,"rank":328},{"article":"Sebastián_Marroquín","views":16259,"rank":329},{"article":"Kim_Jong-un","views":16237,"rank":330},{"article":"The_Maze_Runner","views":16217,"rank":331},{"article":"Leonardo_DiCaprio","views":16111,"rank":332},{"article":"Coen_brothers","views":16097,"rank":333},{"article":"List_of_Gotham_episodes","views":16079,"rank":334},{"article":"Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License","views":16064,"rank":335},{"article":"Overtoun_Bridge","views":16050,"rank":336},{"article":"Kate_Mara","views":16009,"rank":337},{"article":"Marvel_Cinematic_Universe","views":16006,"rank":338},{"article":"Che_Guevara","views":15958,"rank":339},{"article":"XXX","views":15942,"rank":340},{"article":"File:Gummy_bears.jpg","views":15912,"rank":341},{"article":"China","views":15885,"rank":342},{"article":"Supernatural_(U.S._TV_series)","views":15850,"rank":343},{"article":"Mila_Kunis","views":15782,"rank":344},{"article":"Brian_Wilson","views":15728,"rank":345},{"article":"American_Horror_Story:_Asylum","views":15724,"rank":346},{"article":"Maximilian_Kolbe","views":15707,"rank":347},{"article":"Limitless_(TV_series)","views":15704,"rank":348},{"article":"Paul_Prudhomme","views":15680,"rank":349},{"article":"List_of_highest-grossing_films","views":15628,"rank":350},{"article":"Descendants_(2015_film)","views":15601,"rank":351},{"article":"Joseph_Gordon-Levitt","views":15593,"rank":352},{"article":"Insidious_(film)","views":15544,"rank":353},{"article":"Patrick_Swayze","views":15524,"rank":354},{"article":"Blindspot_(TV_series)","views":15509,"rank":355},{"article":"Insidious:_Chapter_3","views":15490,"rank":356},{"article":"My_Little_Pony:_Friendship_Is_Magic_(season_5)","views":15486,"rank":357},{"article":"Doc_Holliday","views":15474,"rank":358},{"article":"Apple_Inc.","views":15472,"rank":359},{"article":"Star_Wars:_Battlefront","views":15465,"rank":360},{"article":"Until_Dawn","views":15458,"rank":361},{"article":"Southpaw_(film)","views":15453,"rank":362},{"article":"Sex","views":15420,"rank":363},{"article":"Democratic_Party_presidential_debates,_2016","views":15405,"rank":364},{"article":"Voynich_manuscript","views":15387,"rank":365},{"article":"U.S._Route_41_Business_(Marquette,_Michigan)","views":15364,"rank":366},{"article":"Paul_Walker","views":15362,"rank":367},{"article":"Aishwarya_Rai_Bachchan","views":15335,"rank":368},{"article":"Alan_Turing","views":15327,"rank":369},{"article":"Grey's_Anatomy","views":15323,"rank":370},{"article":"Unit_731","views":15301,"rank":371},{"article":"Syria","views":15284,"rank":372},{"article":"List_of_school_shootings_in_the_United_States","views":15211,"rank":373},{"article":"Sexual_intercourse","views":15209,"rank":374},{"article":"Jennifer_Aniston","views":15187,"rank":375},{"article":"Vin_Diesel","views":15184,"rank":376},{"article":"1996_Mount_Everest_disaster","views":15145,"rank":377},{"article":"Whoopi_Goldberg","views":15053,"rank":378},{"article":"Tom_Hanks","views":14998,"rank":379},{"article":"Koopsta_Knicca","views":14984,"rank":380},{"article":"Continuum_(TV_series)","views":14969,"rank":381},{"article":"Terminator_Genisys","views":14918,"rank":382},{"article":"Homeland_(season_5)","views":14896,"rank":383},{"article":"Eobard_Thawne","views":14882,"rank":384},{"article":"Richard_Gere","views":14869,"rank":385},{"article":"List_of_James_Bond_films","views":14798,"rank":386},{"article":"Emily_Blunt","views":14781,"rank":387},{"article":"Germany","views":14780,"rank":388},{"article":"Kanye_West","views":14755,"rank":389},{"article":"Elvis_Presley","views":14694,"rank":390},{"article":"Wyatt_Earp","views":14676,"rank":391},{"article":"Chanel_West_Coast","views":14667,"rank":392},{"article":"Rooney_Mara","views":14666,"rank":393},{"article":"List_of_highest-grossing_Indian_films","views":14644,"rank":394},{"article":"Tomorrowland_(film)","views":14642,"rank":395},{"article":"List_of_Reign_(TV_series)_episodes","views":14638,"rank":396},{"article":"Suicide_Squad_(film)","views":14627,"rank":397},{"article":"Kevin_McCarthy_(California_politician)","views":14610,"rank":398},{"article":"Reverse-Flash","views":14599,"rank":399},{"article":"Death_of_Elisa_Lam","views":14592,"rank":400},{"article":"Angelina_Jolie","views":14570,"rank":401},{"article":"2018_FIFA_World_Cup_qualification","views":14567,"rank":402},{"article":"Supernatural_(season_11)","views":14553,"rank":403},{"article":"Major_League_Baseball_postseason","views":14544,"rank":404},{"article":"Meryl_Streep","views":14519,"rank":405},{"article":"MC_Hammer","views":14493,"rank":406},{"article":"Channing_Tatum","views":14491,"rank":407},{"article":"2015_Men's_European_Volleyball_Championship","views":14462,"rank":408},{"article":"Arnold_Schwarzenegger","views":14404,"rank":409},{"article":"Rita_Ora","views":14398,"rank":410},{"article":"Donald_Glover","views":14318,"rank":411},{"article":"Attack_on_Titan","views":14298,"rank":412},{"article":"Ridley_Scott","views":14293,"rank":413},{"article":"Special:LinkSearch","views":14283,"rank":414},{"article":"Bill_Gates","views":14256,"rank":415},{"article":"The_Originals_(TV_series)","views":14248,"rank":416},{"article":"Thanksgiving_(Canada)","views":14242,"rank":417},{"article":"Daniel_Craig","views":14239,"rank":418},{"article":"American_Horror_Story:_Coven","views":14204,"rank":419},{"article":"Israel","views":14165,"rank":420},{"article":"Dope_(film)","views":14164,"rank":421},{"article":"Ariana_Grande","views":14164,"rank":421},{"article":"Tom_Hiddleston","views":14154,"rank":423},{"article":"Kellie_Bright","views":14138,"rank":424},{"article":"Aladdin_(1992_Disney_film)","views":14132,"rank":425},{"article":"New_York_City","views":14108,"rank":426},{"article":"Japan","views":14101,"rank":427},{"article":"Peter_Andre","views":14074,"rank":428},{"article":"Charge_(warfare)","views":14041,"rank":429},{"article":"Amy_Schumer","views":14026,"rank":430},{"article":"Agents_of_S.H.I.E.L.D.","views":14011,"rank":431},{"article":"David_Beckham","views":13985,"rank":432},{"article":"Tu_Youyou","views":13962,"rank":433},{"article":"John_Lackey","views":13909,"rank":434},{"article":"Dr._Ken","views":13905,"rank":435},{"article":"Amber_Rose","views":13890,"rank":436},{"article":"Exodus:_Gods_and_Kings","views":13836,"rank":437},{"article":"Special:RecentChangesLinked","views":13834,"rank":438},{"article":"Curse_of_the_Billy_Goat","views":13823,"rank":439},{"article":"Bruce_Lee","views":13796,"rank":440},{"article":"Canadian_federal_election,_2015","views":13747,"rank":441},{"article":"Mars","views":13723,"rank":442},{"article":"Template:Syrian_Civil_War_detailed_map","views":13716,"rank":443},{"article":"Mission:_Impossible_–_Rogue_Nation","views":13700,"rank":444},{"article":"Hailee_Steinfeld","views":13696,"rank":445},{"article":"Sarah_Paulson","views":13677,"rank":446},{"article":"Benicio_del_Toro","views":13672,"rank":447},{"article":"Hawaii_Five-0","views":13642,"rank":448},{"article":"Enfield_Poltergeist","views":13639,"rank":449},{"article":"Mother_Teresa","views":13629,"rank":450},{"article":"Edward_Snowden","views":13600,"rank":451},{"article":"The_Amazing_Race_27","views":13598,"rank":452},{"article":"Natalie_Portman","views":13590,"rank":453},{"article":"Ant-Man_(film)","views":13581,"rank":454},{"article":"Ben_Affleck","views":13580,"rank":455},{"article":"List_of_American_Horror_Story_episodes","views":13568,"rank":456},{"article":"List_of_Castle_episodes","views":13557,"rank":457},{"article":"Pornhub","views":13502,"rank":458},{"article":"Being_John_Malkovich","views":13477,"rank":459},{"article":"Rihanna","views":13464,"rank":460},{"article":"Kelly–Hopkinsville_encounter","views":13438,"rank":461},{"article":"Singapore","views":13437,"rank":462},{"article":"Lorenza_Izzo","views":13416,"rank":463},{"article":"Matt_Hasselbeck","views":13413,"rank":464},{"article":"Before_the_Flood_(Doctor_Who)","views":13406,"rank":465},{"article":"Illuminati","views":13394,"rank":466},{"article":"Anne_Hathaway","views":13362,"rank":467},{"article":"Ken_Jennings","views":13354,"rank":468},{"article":"List_of_How_to_Get_Away_with_Murder_episodes","views":13351,"rank":469},{"article":"James_Franco","views":13348,"rank":470},{"article":"American_Sniper","views":13343,"rank":471},{"article":"Tito_Jackson","views":13339,"rank":472},{"article":"Leif_Erikson_Day","views":13283,"rank":473},{"article":"Anton_du_Beke","views":13280,"rank":474},{"article":"Brad_Pitt","views":13249,"rank":475},{"article":"Far_Cry_Primal","views":13229,"rank":476},{"article":"Garrett_Hedlund","views":13200,"rank":477},{"article":"1933_United_Airlines_Boeing_247_mid-air_explosion","views":13200,"rank":477},{"article":"John_F._Kennedy","views":13198,"rank":479},{"article":"Keegan-Michael_Key","views":13178,"rank":480},{"article":"Denis_O'Hare","views":13153,"rank":481},{"article":"Snoop_Dogg","views":13150,"rank":482},{"article":"Scandal_(TV_series)","views":13133,"rank":483},{"article":"Vision_(Marvel_Comics)","views":13125,"rank":484},{"article":"Leonard_Fournette","views":13118,"rank":485},{"article":"Jerry_Parr","views":13102,"rank":486},{"article":"1972_Andes_flight_disaster","views":13096,"rank":487},{"article":"Finn_Wittrock","views":13082,"rank":488},{"article":"Joker_(comics)","views":13042,"rank":489},{"article":"Anushka_Shetty","views":13024,"rank":490},{"article":"Insidious:_Chapter_2","views":13016,"rank":491},{"article":"Mark_Zuckerberg","views":13000,"rank":492},{"article":"Anthea_Turner","views":12976,"rank":493},{"article":"XXXX","views":12952,"rank":494},{"article":"The_Beatles","views":12952,"rank":494},{"article":"Shah_Rukh_Khan","views":12951,"rank":496},{"article":"Justin_Trudeau","views":12924,"rank":497},{"article":"Suge_Knight","views":12918,"rank":498},{"article":"List_of_Walt_Disney_Pictures_films","views":12900,"rank":499},{"article":"Seven_deadly_sins","views":12891,"rank":500},{"article":"Akshay_Kumar","views":12871,"rank":501},{"article":"St._Louis_Cardinals","views":12862,"rank":502},{"article":"Pretty_Little_Liars_(TV_series)","views":12829,"rank":503},{"article":"The_X_Factor_(UK_series_12)","views":12820,"rank":504},{"article":"Pornography","views":12805,"rank":505},{"article":"Wales_national_football_team","views":12790,"rank":506},{"article":"List_of_The_Blacklist_episodes","views":12787,"rank":507},{"article":"Steve_Wozniak","views":12782,"rank":508},{"article":"Amitabh_Bachchan","views":12768,"rank":509},{"article":"The_Maze_Runner_(film)","views":12759,"rank":510},{"article":"Wonders_of_the_World","views":12755,"rank":511},{"article":"Metal_Gear_Solid_V:_The_Phantom_Pain","views":12725,"rank":512},{"article":"Max_Headroom_broadcast_signal_intrusion","views":12713,"rank":513},{"article":"Bradley_Cooper","views":12712,"rank":514},{"article":"The_Knick","views":12697,"rank":515},{"article":"Henry_VIII_of_England","views":12693,"rank":516},{"article":"Sylvia_Plath","views":12678,"rank":517},{"article":"Will_Smith","views":12671,"rank":518},{"article":"List_of_highest-grossing_Bollywood_films","views":12670,"rank":519},{"article":"Halsey_(singer)","views":12667,"rank":520},{"article":"Evi_Quaid","views":12656,"rank":521},{"article":"List_of_The_Big_Bang_Theory_episodes","views":12653,"rank":522},{"article":"Alia_Bhatt","views":12650,"rank":523},{"article":"Nicki_Minaj","views":12628,"rank":524},{"article":"Three_6_Mafia","views":12617,"rank":525},{"article":"Cecil_Hotel_(Los_Angeles)","views":12601,"rank":526},{"article":"Marilyn_Monroe","views":12562,"rank":527},{"article":"Gary_Speed","views":12559,"rank":528},{"article":"Flash_(comics)","views":12558,"rank":529},{"article":"Attack_on_Titan_(film)","views":12554,"rank":530},{"article":"The_Undertaker","views":12543,"rank":531},{"article":"Jamelia","views":12467,"rank":532},{"article":"Rob_Hall","views":12452,"rank":533},{"article":"United_States_presidential_election,_2016","views":12444,"rank":534},{"article":"Lycos","views":12441,"rank":535},{"article":"Chris_Pratt","views":12439,"rank":536},{"article":"5-hour_Energy","views":12439,"rank":536},{"article":"Istanbul","views":12434,"rank":538},{"article":"UEFA_Euro_2016_qualifying_Group_H","views":12431,"rank":539},{"article":"Asperger_syndrome","views":12410,"rank":540},{"article":"Abraham_Lincoln","views":12384,"rank":541},{"article":"The_Affair_(TV_series)","views":12358,"rank":542},{"article":"Vietnam_War","views":12357,"rank":543},{"article":"List_of_Suits_episodes","views":12344,"rank":544},{"article":"James_Storm","views":12340,"rank":545},{"article":"Furious_7","views":12338,"rank":546},{"article":"Breaking_Bad","views":12331,"rank":547},{"article":"Star_Wars_Episode_II:_Attack_of_the_Clones","views":12314,"rank":548},{"article":"Thanksgiving","views":12308,"rank":549},{"article":"Jake_Gyllenhaal","views":12297,"rank":550},{"article":"Dragon_Ball_Super","views":12293,"rank":551},{"article":"Uber_(company)","views":12292,"rank":552},{"article":"Robert_Lewandowski","views":12285,"rank":553},{"article":"Brie_Larson","views":12285,"rank":553},{"article":"Marisa_Tomei","views":12276,"rank":555},{"article":"Patagonia","views":12268,"rank":556},{"article":"Heroes_(TV_series)","views":12243,"rank":557},{"article":"Faisal_Khan_(actor)","views":12240,"rank":558},{"article":"Enrique_Gratas","views":12218,"rank":559},{"article":"List_of_The_Nanny_episodes","views":12194,"rank":560},{"article":"Flash_(Barry_Allen)","views":12192,"rank":561},{"article":"How_to_Get_Away_with_Murder_(season_2)","views":12178,"rank":562},{"article":"Android_version_history","views":12170,"rank":563},{"article":"Kendall_Jenner","views":12146,"rank":564},{"article":"Wicked_City_(TV_series)","views":12143,"rank":565},{"article":"Sylvester_Stallone","views":12135,"rank":566},{"article":"Pride_and_Prejudice_and_Zombies","views":12125,"rank":567},{"article":"Pakistan","views":12105,"rank":568},{"article":"Lil_Wayne","views":12102,"rank":569},{"article":"Ed_Sheeran","views":12076,"rank":570},{"article":"Person_of_Interest_(TV_series)","views":12075,"rank":571},{"article":"Clint_Eastwood","views":12072,"rank":572},{"article":"Taissa_Farmiga","views":12055,"rank":573},{"article":"National_League_Division_Series","views":12049,"rank":574},{"article":"Kane_(wrestler)","views":12041,"rank":575},{"article":"List_of_The_Vampire_Diaries_episodes","views":12026,"rank":576},{"article":"Day_of_the_Dead","views":12015,"rank":577},{"article":"Sherlock_(TV_series)","views":11987,"rank":578},{"article":"Azerbaijan","views":11978,"rank":579},{"article":"James_Spader","views":11975,"rank":580},{"article":"Bob_Marley","views":11964,"rank":581},{"article":"New_Zealand","views":11947,"rank":582},{"article":"Portal:Contents","views":11945,"rank":583},{"article":"The_Gift_(2015_film)","views":11941,"rank":584},{"article":"Adam_Sandler","views":11929,"rank":585},{"article":"London","views":11917,"rank":586},{"article":"Vice_President_of_the_United_States","views":11912,"rank":587},{"article":"Islam","views":11863,"rank":588},{"article":"Sultan_(2016_film)","views":11861,"rank":589},{"article":"Charles_Manson","views":11826,"rank":590},{"article":"September_11_attacks","views":11823,"rank":591},{"article":"Sam_Allardyce","views":11821,"rank":592},{"article":"Friends","views":11811,"rank":593},{"article":"Norman_Reedus","views":11811,"rank":593},{"article":"Gordon_Honeycombe","views":11810,"rank":595},{"article":"Michael_Jordan","views":11799,"rank":596},{"article":"Norm_Cash","views":11797,"rank":597},{"article":"Agents_of_S.H.I.E.L.D._(season_3)","views":11783,"rank":598},{"article":"Orange_Is_the_New_Black","views":11772,"rank":599},{"article":"Peter_Pan","views":11770,"rank":600},{"article":"Masturbation","views":11763,"rank":601},{"article":"Alexander_the_Great","views":11728,"rank":602},{"article":"Greek_alphabet","views":11714,"rank":603},{"article":"Batman","views":11713,"rank":604},{"article":"Moses","views":11703,"rank":605},{"article":"Hugh_Jackman","views":11674,"rank":606},{"article":"Ana_de_Armas","views":11665,"rank":607},{"article":"Emma_Watson","views":11645,"rank":608},{"article":"List_of_American_Horror_Story_characters","views":11634,"rank":609},{"article":"Freddie_Mercury","views":11582,"rank":610},{"article":"Android_(operating_system)","views":11577,"rank":611},{"article":"Scream_(TV_series)","views":11561,"rank":612},{"article":"Batman_v_Superman:_Dawn_of_Justice","views":11548,"rank":613},{"article":"RMS_Titanic","views":11540,"rank":614},{"article":"Kazakhstan","views":11539,"rank":615},{"article":"Al_Capone","views":11536,"rank":616},{"article":"France","views":11501,"rank":617},{"article":"Category:Living_people","views":11491,"rank":618},{"article":"The_Revenant_(2015_film)","views":11473,"rank":619},{"article":"Margaret_Thatcher","views":11466,"rank":620},{"article":"George_W._Bush","views":11458,"rank":621},{"article":"The_Book_of_Eli","views":11458,"rank":621},{"article":"Angelababy","views":11454,"rank":623},{"article":"Dilwale_(2015_film)","views":11453,"rank":624},{"article":"Edward_Mordake","views":11447,"rank":625},{"article":"Bourne_(film_series)","views":11440,"rank":626},{"article":"Hilary_Duff","views":11421,"rank":627},{"article":"Wikipedia:Your_first_article","views":11419,"rank":628},{"article":"Ashton_Kutcher","views":11411,"rank":629},{"article":"House_of_Cards_(U.S._TV_series)","views":11409,"rank":630},{"article":"Star_Wars_Rebels","views":11387,"rank":631},{"article":"Guardians_of_the_Galaxy_(film)","views":11381,"rank":632},{"article":"Borussia_Dortmund","views":11381,"rank":632},{"article":"Paper_Towns_(film)","views":11380,"rank":634},{"article":"Shaquille_O'Neal","views":11370,"rank":635},{"article":"New_York_Mets","views":11357,"rank":636},{"article":"Uruguay","views":11351,"rank":637},{"article":"Liam_Neeson","views":11348,"rank":638},{"article":"Henry_Slade_(rugby_player)","views":11326,"rank":639},{"article":"Nikola_Tesla","views":11311,"rank":640},{"article":"Second_Amendment_to_the_United_States_Constitution","views":11308,"rank":641},{"article":"Blake_Lively","views":11293,"rank":642},{"article":"England_national_rugby_union_team","views":11280,"rank":643},{"article":"One_Direction","views":11247,"rank":644},{"article":"Alexandra_Daddario","views":11244,"rank":645},{"article":"Jessica_Jones_(TV_series)","views":11239,"rank":646},{"article":"Chloë_Sevigny","views":11236,"rank":647},{"article":"List_of_My_Little_Pony:_Friendship_Is_Magic_episodes","views":11230,"rank":648},{"article":"Steve_Jobs_(film)","views":11204,"rank":649},{"article":"Joseph_Stalin","views":11203,"rank":650},{"article":"Jack_Black","views":11194,"rank":651},{"article":"Legend_(2015_film)","views":11193,"rank":652},{"article":"Ten_Commandments","views":11186,"rank":653},{"article":"Cheyenne_Jackson","views":11149,"rank":654},{"article":"Tom_Selleck","views":11136,"rank":655},{"article":"2011_Rugby_World_Cup","views":11135,"rank":656},{"article":"Elizabeth_Olsen","views":11117,"rank":657},{"article":"Jason_Statham","views":11089,"rank":658},{"article":"Andrew_Sullivan","views":11077,"rank":659},{"article":"Michelle_Rodriguez","views":11076,"rank":660},{"article":"Prabhas","views":11075,"rank":661},{"article":"Assassin's_Creed","views":11051,"rank":662},{"article":"Emma_Stone","views":11041,"rank":663},{"article":"Suits_(TV_series)","views":11029,"rank":664},{"article":"André_the_Giant","views":11024,"rank":665},{"article":"Kaley_Cuoco","views":11022,"rank":666},{"article":"Owen_Farrell","views":11022,"rank":666},{"article":"England_national_football_team","views":11017,"rank":668},{"article":"Human_penis_size","views":11003,"rank":669},{"article":"Vijay_(actor)","views":10993,"rank":670},{"article":"Dubai","views":10977,"rank":671},{"article":"The_Wanted","views":10965,"rank":672},{"article":"She_Was_Pretty","views":10962,"rank":673},{"article":"Pink_Floyd","views":10950,"rank":674},{"article":"South_Park_(season_19)","views":10948,"rank":675},{"article":"Attempted_assassination_of_Ronald_Reagan","views":10935,"rank":676},{"article":"Robert_Downey,_Jr.","views":10930,"rank":677},{"article":"List_of_Fairy_Tail_episodes","views":10917,"rank":678},{"article":"David_Carradine","views":10909,"rank":679},{"article":"Miley_Cyrus","views":10889,"rank":680},{"article":"The_Man_in_the_High_Castle","views":10879,"rank":681},{"article":"Nobel_Prize","views":10860,"rank":682},{"article":"Sand_dollar","views":10833,"rank":683},{"article":"Philippines","views":10831,"rank":684},{"article":"The_Green_Inferno_(film)","views":10813,"rank":685},{"article":"Harley_Quinn","views":10812,"rank":686},{"article":"Hugh_Scully","views":10808,"rank":687},{"article":"Madonna_(entertainer)","views":10799,"rank":688},{"article":"Special:Log","views":10794,"rank":689},{"article":"UEFA_Euro_2016_qualifying_play-offs","views":10785,"rank":690},{"article":"Phil_Tufnell","views":10772,"rank":691},{"article":"Michelle_Borth","views":10770,"rank":692},{"article":"Jackie_Chan","views":10768,"rank":693},{"article":"Nina_Dobrev","views":10768,"rank":693},{"article":"Jim_Harbaugh","views":10761,"rank":695},{"article":"Frank_Sinatra","views":10752,"rank":696},{"article":"Ennu_Ninte_Moideen","views":10741,"rank":697},{"article":"Bill_Clinton","views":10720,"rank":698},{"article":"Sama-Bajau_peoples","views":10715,"rank":699},{"article":"William_Shakespeare","views":10715,"rank":699},{"article":"Netherlands","views":10706,"rank":701},{"article":"William_M._Bulger","views":10695,"rank":702},{"article":"Scientology","views":10695,"rank":702},{"article":"Kaz_II","views":10682,"rank":704},{"article":"Capgras_delusion","views":10681,"rank":705},{"article":"Twitter","views":10678,"rank":706},{"article":"Shaandaar","views":10676,"rank":707},{"article":"Robert_Kardashian","views":10674,"rank":708},{"article":"England","views":10642,"rank":709},{"article":"Kylie_Jenner","views":10642,"rank":709},{"article":"Bridgit_Mendler","views":10640,"rank":711},{"article":"Julia_Roberts","views":10640,"rank":711},{"article":"Jamaica_ginger","views":10636,"rank":713},{"article":"United_Arab_Emirates","views":10632,"rank":714},{"article":"Legends_of_Tomorrow","views":10625,"rank":715},{"article":"Maya_Moore","views":10605,"rank":716},{"article":"Muhammad_Ali","views":10600,"rank":717},{"article":"Bipolar_disorder","views":10599,"rank":718},{"article":"Jeff_Daniels","views":10589,"rank":719},{"article":"Aliona_Vilani","views":10589,"rank":719},{"article":"Spy_(2015_film)","views":10584,"rank":721},{"article":"The_Big_Bang_Theory_(season_9)","views":10566,"rank":722},{"article":"Tom_Brady","views":10566,"rank":722},{"article":"Periodic_table","views":10560,"rank":724},{"article":"California","views":10558,"rank":725},{"article":"Rose_Byrne","views":10558,"rank":725},{"article":"Rock_Band_4","views":10554,"rank":727},{"article":"List_of_UFC_events","views":10542,"rank":728},{"article":"Martin_Luther_King,_Jr.","views":10541,"rank":729},{"article":"Johnny_Cash","views":10515,"rank":730},{"article":"Patrick_J._Kennedy","views":10507,"rank":731},{"article":"Audrey_Hepburn","views":10505,"rank":732},{"article":"List_of_countries_by_GDP_(nominal)","views":10501,"rank":733},{"article":"Wikipedia:About","views":10487,"rank":734},{"article":"DC_Universe_Animated_Original_Movies","views":10453,"rank":735},{"article":"Downton_Abbey","views":10451,"rank":736},{"article":"Josh_Brolin","views":10448,"rank":737},{"article":"Adam_Levine","views":10447,"rank":738},{"article":"Qatar","views":10442,"rank":739},{"article":"Wales","views":10439,"rank":740},{"article":"2015_Presidents_Cup","views":10439,"rank":740},{"article":"Dark_Matter_(TV_series)","views":10431,"rank":742},{"article":"Shamita_Shetty","views":10429,"rank":743},{"article":"Goosebumps_(film)","views":10427,"rank":744},{"article":"Vagina","views":10425,"rank":745},{"article":"Attack_on_Pearl_Harbor","views":10410,"rank":746},{"article":"Saudi_Arabia","views":10392,"rank":747},{"article":"Irrfan_Khan","views":10386,"rank":748},{"article":"Greig_Laidlaw","views":10384,"rank":749},{"article":"S._S._Rajamouli","views":10382,"rank":750},{"article":"Diepreye_Alamieyeseigha","views":10359,"rank":751},{"article":"Tamasha_(film)","views":10355,"rank":752},{"article":"Levi_Miller","views":10343,"rank":753},{"article":"Kurt_Cobain","views":10333,"rank":754},{"article":"James_Bond","views":10332,"rank":755},{"article":"UFC_192","views":10303,"rank":756},{"article":"Saturday_Morning_Breakfast_Cereal","views":10294,"rank":757},{"article":"Jessie_(TV_series)","views":10289,"rank":758},{"article":"South_Park","views":10261,"rank":759},{"article":"Hong_Kong","views":10257,"rank":760},{"article":"Stephen_Harper","views":10251,"rank":761},{"article":"Netherlands_national_football_team","views":10244,"rank":762},{"article":"Steve_McQueen","views":10242,"rank":763},{"article":"Chernobyl_disaster","views":10228,"rank":764},{"article":"Anal_sex","views":10226,"rank":765},{"article":"Lana_Del_Rey","views":10225,"rank":766},{"article":"Cotton_Bowl_(stadium)","views":10224,"rank":767},{"article":"World_population","views":10192,"rank":768},{"article":"Netflix","views":10179,"rank":769},{"article":"List_of_Tamil_films_of_2015","views":10154,"rank":770},{"article":"Ivy_League","views":10144,"rank":771},{"article":"Daniel_O'Donnell","views":10141,"rank":772},{"article":"Ryan_Reynolds","views":10133,"rank":773},{"article":"Beastly_(film)","views":10132,"rank":774},{"article":"Rowan_Blanchard","views":10108,"rank":775},{"article":"Hayden_Christensen","views":10104,"rank":776},{"article":"Gwen_Stefani","views":10094,"rank":777},{"article":"Umpqua_Community_College_shooting","views":10090,"rank":778},{"article":"List_of_American_football_stadiums_by_capacity","views":10089,"rank":779},{"article":"Steve_Irwin","views":10079,"rank":780},{"article":"Back_to_the_Future_Part_II","views":10079,"rank":780},{"article":"Keira_Knightley","views":10058,"rank":782},{"article":"UFC_Fight_Night:_Poirier_vs._Duffy","views":10057,"rank":783},{"article":"Taj_Mahal","views":10030,"rank":784},{"article":"Kirsten_Dunst","views":10008,"rank":785},{"article":"Bashar_al-Assad","views":9997,"rank":786},{"article":"Dengue_fever","views":9992,"rank":787},{"article":"Beyoncé","views":9987,"rank":788},{"article":"Jennifer_Lawrence","views":9976,"rank":789},{"article":"Rachel_McAdams","views":9970,"rank":790},{"article":"Deepika_Padukone","views":9959,"rank":791},{"article":"Charlize_Theron","views":9957,"rank":792},{"article":"James_Corden","views":9952,"rank":793},{"article":"Joaquín_Guzmán","views":9948,"rank":794},{"article":"Multiple_sclerosis","views":9944,"rank":795},{"article":"Kourtney_Kardashian","views":9935,"rank":796},{"article":"Bathurst_1000","views":9930,"rank":797},{"article":"Outer_Space_Treaty","views":9919,"rank":798},{"article":"Fantastic_Four_(2015_film)","views":9913,"rank":799},{"article":"Bones_(TV_series)","views":9910,"rank":800},{"article":"Harry_Potter_(film_series)","views":9899,"rank":801},{"article":"Tim_Vine","views":9897,"rank":802},{"article":"John_Travolta","views":9891,"rank":803},{"article":"Rooting_(Android_OS)","views":9886,"rank":804},{"article":"South_Korea","views":9882,"rank":805},{"article":"50_Cent","views":9875,"rank":806},{"article":"Phallus_indusiatus","views":9863,"rank":807},{"article":"The_Hunger_Games","views":9856,"rank":808},{"article":"Kurds","views":9846,"rank":809},{"article":"John_Connolly_(FBI)","views":9845,"rank":810},{"article":"Emilia_Clarke","views":9831,"rank":811},{"article":"The_Beach_Boys","views":9826,"rank":812},{"article":"Wayne_Rooney","views":9798,"rank":813},{"article":"Kakatiya_dynasty","views":9797,"rank":814},{"article":"Idris_Elba","views":9783,"rank":815},{"article":"List_of_The_Originals_episodes","views":9779,"rank":816},{"article":"Pirates_of_the_Caribbean:_On_Stranger_Tides","views":9776,"rank":817},{"article":"Sukhoi_Su-34","views":9776,"rank":817},{"article":"Ottoman_Empire","views":9760,"rank":819},{"article":"Ted_Bundy","views":9717,"rank":820},{"article":"Z_Nation","views":9715,"rank":821},{"article":"Éder_Citadin_Martins","views":9710,"rank":822},{"article":"Pirates_of_the_Caribbean:_Dead_Men_Tell_No_Tales","views":9708,"rank":823},{"article":"List_of_United_States_cities_by_population","views":9707,"rank":824},{"article":"English_language","views":9699,"rank":825},{"article":"Melania_Trump","views":9697,"rank":826},{"article":"Jennifer_Garner","views":9693,"rank":827},{"article":"UEFA_Euro_2016_qualifying_Group_D","views":9688,"rank":828},{"article":"Jerry_Rice","views":9687,"rank":829},{"article":"Ernest_Moniz","views":9684,"rank":830},{"article":"Walt_Disney","views":9674,"rank":831},{"article":"Tesla_Motors","views":9671,"rank":832},{"article":"Nancy_Reagan","views":9637,"rank":833},{"article":"Andorra","views":9628,"rank":834},{"article":"Neem_Karoli_Baba","views":9626,"rank":835},{"article":"Ruby_Rose","views":9626,"rank":835},{"article":"Harry_Houdini","views":9619,"rank":837},{"article":"Brock_Lesnar","views":9607,"rank":838},{"article":"Sundar_Pichai","views":9601,"rank":839},{"article":"Youtube","views":9599,"rank":840},{"article":"Minions_(film)","views":9597,"rank":841},{"article":"Chris_Hemsworth","views":9597,"rank":841},{"article":"Minecraft","views":9595,"rank":843},{"article":"Lauren_Gottlieb","views":9593,"rank":844},{"article":"Iceland","views":9593,"rank":844},{"article":"Fifty_Shades_of_Grey","views":9589,"rank":846},{"article":"Guillermo_del_Toro","views":9583,"rank":847},{"article":"Pyaar_Ka_Punchnama_2","views":9566,"rank":848},{"article":"Rob_Thomas_(musician)","views":9563,"rank":849},{"article":"South_Africa","views":9557,"rank":850},{"article":"Kate_Hudson","views":9548,"rank":851},{"article":"Pride_and_Prejudice_and_Zombies_(film)","views":9546,"rank":852},{"article":"Solar_System","views":9546,"rank":852},{"article":"Switzerland","views":9531,"rank":854},{"article":"Vedalam","views":9530,"rank":855},{"article":"List_of_Hindi_film_clans","views":9527,"rank":856},{"article":"Chris_Evans_(actor)","views":9524,"rank":857},{"article":"Los_Angeles","views":9522,"rank":858},{"article":"United_States_presidential_line_of_succession","views":9516,"rank":859},{"article":"Sons_of_Anarchy","views":9515,"rank":860},{"article":"Darth_Vader","views":9506,"rank":861},{"article":"Elizabeth_Banks","views":9503,"rank":862},{"article":"The_Player_(2015_TV_series)","views":9498,"rank":863},{"article":"Zoë_Kravitz","views":9494,"rank":864},{"article":"BDSM","views":9478,"rank":865},{"article":"Kate_Winslet","views":9467,"rank":866},{"article":"List_of_Game_of_Thrones_episodes","views":9465,"rank":867},{"article":"Naturism","views":9463,"rank":868},{"article":"Scott_Foley","views":9455,"rank":869},{"article":"Queen_Victoria","views":9454,"rank":870},{"article":"Christian_Bale","views":9451,"rank":871},{"article":"Bryce_Dallas_Howard","views":9448,"rank":872},{"article":"Nigella_Lawson","views":9447,"rank":873},{"article":"3M-54_Klub","views":9443,"rank":874},{"article":"Benedict_Cumberbatch","views":9425,"rank":875},{"article":"Jonny_Wilkinson","views":9420,"rank":876},{"article":"Thomas_Edison","views":9418,"rank":877},{"article":"Once_Upon_a_Time_(season_5)","views":9413,"rank":878},{"article":"Medellín_Cartel","views":9407,"rank":879},{"article":"Kevin_Corcoran","views":9396,"rank":880},{"article":"Naruto","views":9395,"rank":881},{"article":"Pitch_Perfect_2","views":9390,"rank":882},{"article":"Muhammad","views":9389,"rank":883},{"article":"Downtown_(Macklemore_&_Ryan_Lewis_song)","views":9389,"rank":883},{"article":"Zlatan_Ibrahimović","views":9385,"rank":885},{"article":"UEFA_Euro_2016_qualifying_Group_C","views":9385,"rank":885},{"article":"Elizabeth_Taylor","views":9384,"rank":887},{"article":"The_Final_Girls","views":9380,"rank":888},{"article":"The_100_(TV_series)","views":9372,"rank":889},{"article":"2019_Rugby_World_Cup","views":9367,"rank":890},{"article":"Jordan_Lukaku","views":9364,"rank":891},{"article":"Diplocaulus","views":9364,"rank":891},{"article":"Hillary_Clinton","views":9359,"rank":893},{"article":"Fallout_4","views":9354,"rank":894},{"article":"Young_Thug","views":9351,"rank":895},{"article":"The_Pirate_Bay","views":9344,"rank":896},{"article":"2015_CONCACAF_Men's_Olympic_Qualifying_Championship","views":9336,"rank":897},{"article":"The_X_Factor_(UK_TV_series)","views":9329,"rank":898},{"article":"Eli_Roth","views":9325,"rank":899},{"article":"Millennials","views":9316,"rank":900},{"article":"Daylight_saving_time","views":9312,"rank":901},{"article":"Supergirl_(U.S._TV_series)","views":9312,"rank":901},{"article":"Thanos","views":9309,"rank":903},{"article":"Ellie_Goulding","views":9308,"rank":904},{"article":"Parrying_dagger","views":9299,"rank":905},{"article":"Schizophrenia","views":9290,"rank":906},{"article":"Neil_Patrick_Harris","views":9283,"rank":907},{"article":"Supernatural_(season_10)","views":9280,"rank":908},{"article":"The_Departed","views":9275,"rank":909},{"article":"Amber_Heard","views":9268,"rank":910},{"article":"List_of_Gravity_Falls_episodes","views":9266,"rank":911},{"article":"Bella_Thorne","views":9264,"rank":912},{"article":"Matthew_Shepard","views":9260,"rank":913},{"article":"X-Men:_Apocalypse","views":9252,"rank":914},{"article":"Lisa_Ann","views":9251,"rank":915},{"article":"M25_sniper_rifle","views":9239,"rank":916},{"article":"Coen_brothers_filmography","views":9238,"rank":917},{"article":"Joe_Pesci","views":9237,"rank":918},{"article":"Marvin_Gaye","views":9235,"rank":919},{"article":"Lily_Rabe","views":9229,"rank":920},{"article":"George_Clooney","views":9227,"rank":921},{"article":"Allu_Arjun","views":9226,"rank":922},{"article":"Nicolas_Cage","views":9223,"rank":923},{"article":"American_Civil_War","views":9216,"rank":924},{"article":"The_Voice_(U.S._TV_series)","views":9215,"rank":925},{"article":"Johnny_Galecki","views":9208,"rank":926},{"article":"Joe_Maddon","views":9196,"rank":927},{"article":"MDMA","views":9195,"rank":928},{"article":"Blue_Bloods_(TV_series)","views":9188,"rank":929},{"article":"Brazil","views":9185,"rank":930},{"article":"Michael_J._Fox","views":9184,"rank":931},{"article":"Oktoberfest","views":9184,"rank":931},{"article":"Mike_Matheny","views":9181,"rank":933},{"article":"Christopher_Reeve","views":9178,"rank":934},{"article":"Diana,_Princess_of_Wales","views":9177,"rank":935},{"article":"Mel_Gibson","views":9170,"rank":936},{"article":"Bihar_Legislative_Assembly_election,_2015","views":9166,"rank":937},{"article":"Columbine_High_School_massacre","views":9149,"rank":938},{"article":"Jhalak_Dikhhla_Jaa","views":9138,"rank":939},{"article":"Hayden_Panettiere","views":9137,"rank":940},{"article":"Armenia","views":9137,"rank":940},{"article":"Frozen_(2013_film)","views":9132,"rank":942},{"article":"List_of_people_who_died_climbing_Mount_Everest","views":9122,"rank":943},{"article":"Systemic_lupus_erythematosus","views":9121,"rank":944},{"article":"Cameron_Diaz","views":9104,"rank":945},{"article":"The_Walking_Dead_(season_4)","views":9100,"rank":946},{"article":"Al_Pacino","views":9096,"rank":947},{"article":"The_Avengers_(2012_film)","views":9094,"rank":948},{"article":"The_Great_British_Bake_Off","views":9092,"rank":949},{"article":"The_Man_in_the_High_Castle_(TV_series)","views":9087,"rank":950},{"article":"Wikipedia:General_disclaimer","views":9087,"rank":950},{"article":"Sandra_Bullock","views":9084,"rank":952},{"article":"Marilyn_Manson","views":9083,"rank":953},{"article":"Angela_Bassett","views":9082,"rank":954},{"article":"3T","views":9078,"rank":955},{"article":"Modern_Family","views":9078,"rank":955},{"article":"NCIS_(TV_series)","views":9077,"rank":957},{"article":"Helen_George","views":9068,"rank":958},{"article":"Katrina_Kaif","views":9067,"rank":959},{"article":"Narcissistic_personality_disorder","views":9063,"rank":960},{"article":"Criminal_Minds","views":9062,"rank":961},{"article":"Bed_size","views":9061,"rank":962},{"article":"Spain","views":9054,"rank":963},{"article":"Trevor_Noah","views":9048,"rank":964},{"article":"Leonardo_da_Vinci","views":9033,"rank":965},{"article":"K_(anime)","views":9022,"rank":966},{"article":"Tonga","views":9017,"rank":967},{"article":"David_Bowie","views":9017,"rank":967},{"article":"AMBER_Alert","views":9013,"rank":969},{"article":"Bindi_Irwin","views":9003,"rank":970},{"article":"Dragon_Ball_Z:_Resurrection_'F'","views":8998,"rank":971},{"article":"Janet_Jackson","views":8998,"rank":971},{"article":"Kevin_Hart","views":8996,"rank":973},{"article":"Charlie_Chaplin","views":8986,"rank":974},{"article":"Gunasekhar","views":8979,"rank":975},{"article":"George_Washington","views":8979,"rank":975},{"article":"Andrew_Lincoln","views":8975,"rank":977},{"article":"Iran","views":8967,"rank":978},{"article":"Fargo_(film)","views":8963,"rank":979},{"article":"Italy_national_football_team","views":8962,"rank":980},{"article":"Joe_Biden","views":8950,"rank":981},{"article":"Battlefield_Earth_(film)","views":8949,"rank":982},{"article":"Cate_Blanchett","views":8948,"rank":983},{"article":"Megan_Fox","views":8946,"rank":984},{"article":"Wiz_Khalifa","views":8945,"rank":985},{"article":"Gareth_Bale","views":8944,"rank":986},{"article":"Hydrogen","views":8934,"rank":987},{"article":"Titanic_(1997_film)","views":8933,"rank":988},{"article":"WrestleMania_XXX","views":8932,"rank":989},{"article":"Bigg_Boss_9","views":8931,"rank":990},{"article":"List_of_Agents_of_S.H.I.E.L.D._episodes","views":8915,"rank":991},{"article":"Geeta_Basra","views":8908,"rank":992},{"article":"Robert_Frost","views":8904,"rank":993},{"article":"The_Death_Cure","views":8902,"rank":994},{"article":"Jesus","views":8896,"rank":995},{"article":"Bermuda_Triangle","views":8886,"rank":996},{"article":"Keddie_murders","views":8883,"rank":997},{"article":"Back_to_the_Future","views":8881,"rank":998},{"article":"America's_Next_Top_Model","views":8874,"rank":999},{"article":"Napoleon","views":8871,"rank":1000}]}]
}

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]
#

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b
#
def listthem(language):
	biglist = []
	
	thelist = res['query']['namespaces']
	
	for one in thelist:
		if one!='0':
			biglist.append(thelist[one]['*'])
			if 'canonical' in thelist[one]:
				biglist.append(thelist[one]['canonical'])
		
	thelist1 = res['query']['namespacealiases']
	
	for one1 in thelist1:
		biglist.append(one1['*'])
	
	#pywikibot.output(biglist)
	
	return biglist
#


#{"items":[{"project":"en.wikipedia","access":"all-access","year":"2015","month":"10","day":"10","articles":[{"article":"Main_Page","views":18793503,"rank":1}

apipar = {
	"action": "query",
	"format": "json",
	"meta": "siteinfo",
	"siprop": "namespaces|namespacealiases"
}

exclude = {
	'en':{'startswith':('List of'),'exclude':['Main Page']}
}


#

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#

def doSQL(tlistFor,language):
	object = {}
	conn = toolforge.connect(language + 'wiki_p')
	
	groupfd = 0
	for group in chunker(tlistFor,49):
		print(groupfd)
		groupfd += 1
		group = [i.replace("'", "\\'").replace(' ','_') for i in group]
		query = "select p.page_title as page, count(l.ll_lang) from langlinks l join page p on p.page_id=l.ll_from where p.page_title in ('" + "','".join(group) + "') and p.page_namespace=0 and not exists (select * from langlinks m where l.ll_from=m.ll_from and m.ll_lang=\"lv\") group by l.ll_from;"
		query = query.encode('utf-8')
		#print(query)
		try:
			cursor = conn.cursor()
			cursor.execute(query)
			rows = cursor.fetchall()
		except KeyboardInterrupt:
			sys.exit()
		#revids = []
		for row in rows:
			object.update({encode_if_necessary(row[0]).replace('_',' '):encode_if_necessary(row[1])})
	
	return object
#

def removeFromList(list,lang,nspaces):
	excludeAll = exclude[lang]['exclude']
	excludeStarts = exclude[lang]['startswith']
	
	bigmy = []
	for one in pageviewdata["items"][0]["articles"]:
		title = one["article"].replace('_',' ')
		if title.startswith(nspaces): continue
		
		if title.startswith(excludeStarts): continue
		if title in excludeAll: continue
		
		bigmy.append(title)
	pywikibot.output(bigmy[:10])
	
	return bigmy
#
def doAPI(wditems,language):
	r = ''
	idlist = '|'.join(wditems)
	
	r = pywikibot.data.api.Request(site=pywikibot.Site(language, "wikipedia"), lllimit="250",action="query", 
									format = "json",prop="langlinks", titles=idlist,redirects='no').submit()
	
	#pywikibot.output(r)
	return r
#

def get_iwlinks(thelist,lang):
	object = {}
	groupfd=0
	
	for group in chunker(thelist,49):
		print(groupfd)
		groupfd += 1
		apires = doAPI(group,lang)
		entis = apires['query']['pages']
		
		if 'continue' in apires:
			pywikibot.output(apires['continue'])
		
		
		for entdata in entis:
			#pywikibot.output(entis[entdata])
			currData = entis[entdata]
			iws = currData["langlinks"] if "langlinks" in currData else []
			doWeNeed = True
			
			for iw in iws:
				if iw['lang']=='lv':
					doWeNeed = False
					break
			
			if doWeNeed:
				object.update({currData['title']:len(iws)})
	
	return object
	
def one_language(language):
	ns = tuple(listthem(language))
	#https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2015/10/10
	parsedList = removeFromList(pageviewdata["items"][0]["articles"],language,ns)
	afterIws = doSQL(parsedList[:45],language)
	pywikibot.output(afterIws)
	
	WantedArticleList = [[f,afterIws[f]] for f in parsedList if f in afterIws]
	
	filedataREZ = open('lvinfoboxes-gfdgdfgdfgdf.txt', 'w', encoding='utf-8')
	filedataREZ.write(str(WantedArticleList))
	
	
#
one_language('en')