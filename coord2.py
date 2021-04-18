import pywikibot
from pywikibot import pagegenerators
from pywikibot.exceptions import CoordinateGlobeUnknownException


site = pywikibot.Site('lv','wikipedia')

#http://petscan.wmflabs.org/?psid=142680
#http://petscan.wmflabs.org/?psid=802601 - visa Latvija
#http://petscan.wmflabs.org/?psid=879177
listForWork = """
1	Daugavgrīvas iela (Rīga)	113374	(Article)	4791	20180503144123
2	Vecsloboda	129074	(Article)	2009	20180620140044
3	Baltā iela (Rīga)	211596	(Article)	5987	20180414045748
4	Cementa iela	249503	(Article)	3265	20180510143019
5	Rozbeķu pils	257763	(Article)	4445	20180511002356
6	Enkura iela	288744	(Article)	3842	20180606084529
7	Elijas iela	293936	(Article)	2706	20180606084529
8	Biržu (Madonas) muiža	300537	(Article)	1589	20180622223043
9	Astici	315560	(Article)	1939	20180620140046
10	Aklā iela (Rīga)	336895	(Article)	1782	20180504044714
11	Emiļa Melngaiļa iela (Rīga)	338386	(Article)	2421	20180619065600
12	Eiženijas iela (Rīga)	364115	(Article)	1659	20180606084529
13	Līvu laukums	371696	(Article)	1240	20180610102100
14	Edīte	374279	(Article)	1572	20180510093702
15	Raunas luterāņu baznīca	375082	(Article)	9052	20180610210251
16	Puduļu pilskalns	378269	(Article)	3042	20180618224849
17	JCB Kauguru bibliotēka	378440	(Article)	2101	20180509004518
18	Krišupīte	378978	(Article)	1867	20180510093702
19	Lepsturga	379105	(Article)	1713	20180510093702
20	Liepupes-Reiņupes kanāls	379107	(Article)	1990	20180510093702
21	Mazurga	379110	(Article)	1884	20180510093702
22	Muižuļurga	379112	(Article)	1820	20180510093702
23	Noriņa	379114	(Article)	1670	20180513185411
24	Pašupe	379195	(Article)	1622	20180510093702
25	Reisagrāvis	379197	(Article)	1894	20180510093702
26	Vēverupe	379201	(Article)	1831	20180510093702
27	Biķernieki (Seces pagasts)	379930	(Article)	1953	20180620140047
28	Ādmināni	379932	(Article)	2064	20180620140047
29	Biķernieki (Salas pagasts)	379933	(Article)	2119	20180620140047
30	Dolomīts (Salas pagasts)	379936	(Article)	2232	20180620140047
31	Dorškāni	379937	(Article)	2036	20180620140047
32	Dūķernieki	379938	(Article)	2105	20180620140047
33	Gargrode	379939	(Article)	2089	20180620140047
34	Gravāni (Salas pagasts)	379942	(Article)	2208	20180620140047
35	Laši (Ābeļu pagasts)	379984	(Article)	2020	20180620140047
36	Ūziņi	379998	(Article)	2099	20180620140047
37	Jaunplatone	379999	(Article)	2030	20180620140047
38	Bajāri (Jaunsvirlaukas pagasts)	380002	(Article)	2072	20180620140047
39	Jaunsvirlauka	380003	(Article)	2113	20180620140047
40	Vecsvirlauka	380004	(Article)	2041	20180620140047
41	Daugavas gāte	380011	(Article)	1741	20180403215637
42	Gustiņi	380014	(Article)	2054	20180620140047
43	Bloki	380085	(Article)	1550	20180620140047
44	Indrāni (Salas pagasts)	380086	(Article)	2216	20180620140047
45	Kalvāni (Salas pagasts)	380087	(Article)	2185	20180620140047
46	Mālkalni (Salas pagasts)	380088	(Article)	2215	20180620140047
47	Meldernieki	380089	(Article)	2072	20180620140047
48	Muižiņa	380090	(Article)	2088	20180620140047
49	Pēternieki (Salas pagasts)	380138	(Article)	2160	20180620140047
50	Pumpi	380151	(Article)	2099	20180620140047
51	Putnukalni	380153	(Article)	2166	20180620140047
52	Pūteļi	380156	(Article)	2110	20180620140047
53	Radiņi	380157	(Article)	2088	20180620140047
54	Salaspils (Salas pagasts)	380162	(Article)	2160	20180620140047
55	Sankaļi (Salas pagasts)	380168	(Article)	2251	20180620140047
56	Siliņi (Salas pagasts)	380169	(Article)	2160	20180620140047
57	Siliņu stacija	380171	(Article)	2163	20180620140047
58	Smiltaines	380174	(Article)	2157	20180620140047
59	Stuburi	380178	(Article)	2055	20180620140047
60	Zaķi (Salas pagasts)	380179	(Article)	2306	20180620140047
61	Jāņukrogs	380276	(Article)	2042	20180620140047
62	Mazbērstele	380277	(Article)	2081	20180620140047
63	Mazmežotne	380278	(Article)	2154	20180620140047
64	Priedītes	380279	(Article)	2054	20180620140047
65	Punslavas	380324	(Article)	2076	20180620140047
66	Švirkale	380325	(Article)	2053	20180620140047
67	Vecrundāle	380327	(Article)	2089	20180620140047
68	Tīrumi	380362	(Article)	2048	20180620140047
69	Virsīte	380363	(Article)	2131	20180620140047
70	Galzemji	380366	(Article)	2083	20180620140047
71	Grāvendāle	380367	(Article)	2053	20180620140047
72	Vairogi (Viesturu pagasts)	380369	(Article)	2234	20180620140047
73	Virsīte (upe)	380392	(Article)	2367	20180510093702
74	Silinīki (Mērdzenes pagasts)	381589	(Article)	1986	20180620140047
75	Dzērves (Mežvidu pagasts)	381590	(Article)	1952	20180620140047
76	Rogi	381593	(Article)	1991	20180620140047
77	Mujāni	381610	(Article)	3175	20180620140047
78	Bleideļi (Aulejas pagasts)	381629	(Article)	2004	20180620140047
79	Brāslava (Aulejas pagasts)	381630	(Article)	2030	20180620140047
80	Krūgeri	381637	(Article)	2030	20180620140047
81	Kuhari	381638	(Article)	1943	20180620140047
82	Māteji	381641	(Article)	1947	20180620140047
83	Rubeni	381645	(Article)	1996	20180620140047
84	Žaunerāni	381647	(Article)	2008	20180620140047
85	Gorodišče (ciems)	381652	(Article)	1979	20180620140047
86	Ostrovna	381655	(Article)	1990	20180620140047
87	Udinova	381660	(Article)	1966	20180620140047
88	Beržine	381662	(Article)	2005	20180620140047
89	Kalna Boliņi	381666	(Article)	2045	20180620140047
90	Lielie Trūļi	381667	(Article)	2023	20180620140047
91	Mazie Murāni	381672	(Article)	1969	20180620140047
92	Mazie Onzuļi	381676	(Article)	2027	20180620140047
93	Undrukāni	381678	(Article)	1961	20180620140047
94	Andžāni (Kalniešu pagasts)	381679	(Article)	2016	20180620140047
95	Dauguļi (Kalniešu pagasts)	381681	(Article)	2015	20180620140047
96	Dubrovka (Kalniešu pagasts)	381682	(Article)	1961	20180620140047
97	Lielindrica	381684	(Article)	2026	20180620140047
98	Livčāni	381685	(Article)	1965	20180620140047
99	Peļniki	381686	(Article)	2014	20180620140047
100	Podgurje (Kalniešu pagasts)	381688	(Article)	2013	20180620140047
101	Cimoškas (Kombuļu pagasts)	381711	(Article)	1958	20180620140047
102	Banceniškas	381713	(Article)	1974	20180620140047
103	Jadlovci	381715	(Article)	1958	20180620140047
104	Lielie Unguri	381716	(Article)	2026	20180620140047
105	Lielie Zīmaiži	381932	(Article)	2036	20180620140047
106	Škutāni (Kombuļu pagasts)	381933	(Article)	1961	20180620140047
107	Aišpuri (Krāslavas pagasts)	381934	(Article)	1997	20180620140047
108	Krīviņi (Krāslavas pagasts)	381935	(Article)	2051	20180620140047
109	Pastari (Krāslavas pagasts)	381936	(Article)	2042	20180620140047
110	Kiseļevci	381937	(Article)	1965	20180620140047
111	Krivoseļci	381938	(Article)	1968	20180620140047
112	Gromiki	381939	(Article)	2022	20180620140047
113	Podleškova	381940	(Article)	1980	20180620140047
114	Poreči	381941	(Article)	1969	20180620140047
115	Čenčupi	381942	(Article)	1932	20180620140047
116	Grundāni	381943	(Article)	1961	20180620140047
117	Kotolnieki	381944	(Article)	2015	20180620140047
118	Kuliniški	381945	(Article)	2016	20180620140047
119	Ļaksi	381946	(Article)	1948	20180620140047
120	Vanagiški	381947	(Article)	1942	20180620140047
121	Augustiniški	381953	(Article)	2065	20180620140047
122	Dunski (Ūdrīšu pagasts)	381954	(Article)	1990	20180620140047
123	Lejas Romuļi	381955	(Article)	2057	20180620140047
124	Lielie Muļķi	381956	(Article)	2067	20180620140047
125	Misjūni	381958	(Article)	2047	20180620140047
126	Odigjāni	381959	(Article)	2001	20180620140047
127	Rakuti (Ūdrīšu pagasts)	381960	(Article)	1988	20180620140047
128	Skerškāni	381961	(Article)	2056	20180620140047
129	Vilmaņi	381962	(Article)	1992	20180620140047
130	Dzirkaļi (Kūku pagasts)	381984	(Article)	1909	20180620140047
131	Trākši (Variešu pagasts)	381986	(Article)	1916	20180620140047
132	Katvari	382089	(Article)	2041	20180620140047
133	Dobenieki (Rugāju pagasts)	382117	(Article)	2239	20180620140047
134	Nabe (ciems)	382122	(Article)	2054	20180620140047
135	Strodi (Jersikas pagasts)	382164	(Article)	1971	20180620140047
136	Stūrišķi	382167	(Article)	2034	20180620140047
137	Muktupāveli	382168	(Article)	2042	20180620140047
138	Oškalnieši	382169	(Article)	2018	20180620140047
139	Šultes	382170	(Article)	1931	20180620140047
140	Steķi (Turku pagasts)	382171	(Article)	1991	20180620140047
141	Veiguri	382172	(Article)	2013	20180620140047
142	Zepi (Turku pagasts)	382173	(Article)	2011	20180620140047
143	Evertova	382237	(Article)	1929	20180620140047
144	Andži	382239	(Article)	1930	20180620140047
145	Poļu Gorbuni	382241	(Article)	1953	20180620140047
146	Potorova	382242	(Article)	1942	20180620140047
147	Meļņiki	382243	(Article)	1943	20180620140047
148	Šilki	382244	(Article)	1929	20180620140047
149	Divkši	382245	(Article)	1926	20180620140047
150	Dauguļi (Nirzas pagasts)	382248	(Article)	1930	20180620140047
151	Raipole (Nirzas pagasts)	382279	(Article)	1983	20180620140047
152	Gorki (Ņukšu pagasts)	382280	(Article)	1910	20180620140047
153	Juzefinova	382282	(Article)	1967	20180620140047
154	Silovi (Ņukšu pagasts)	382283	(Article)	1899	20180620140047
155	Pešļeva	382997	(Article)	1939	20180620140047
156	Pentjuši	382998	(Article)	1940	20180620140047
157	Kazici	382999	(Article)	1986	20180620140047
158	Gorodoks (Rundēnu pagasts)	383000	(Article)	1936	20180620140047
159	Lubeja (ciems)	383010	(Article)	1961	20180620140047
160	Stūrmežs	383011	(Article)	1971	20180620140047
161	Zvidziena	383012	(Article)	1942	20180620140047
162	Klintaine	383168	(Article)	1993	20180620140047
163	Feldgofa	383176	(Article)	1948	20180620140047
164	Gāgas	383177	(Article)	1914	20180620140047
165	Gubaniški	383178	(Article)	2014	20180620140047
166	Livmaņi	383179	(Article)	1944	20180620140047
167	Maskeviciški	383181	(Article)	1958	20180620140047
168	Rošmoni	383183	(Article)	1994	20180620140047
169	Moskvina	383184	(Article)	2009	20180620140047
170	Asīte	383254	(Article)	1967	20180620140047
171	Leukādijas	383274	(Article)	2013	20180620140047
172	Gatarta	383428	(Article)	1982	20180620140047
173	Meirāni (Bērzgales pagasts)	385123	(Article)	2009	20180620140047
174	Micāni	385137	(Article)	2010	20180620140047
175	Uļinova	385139	(Article)	2009	20180620140047
176	Puncuļi (Čornajas pagasts)	385151	(Article)	1953	20180620140047
177	Rečeņi	385152	(Article)	2009	20180620140047
178	Vagaļi (Čornajas pagasts)	385153	(Article)	2001	20180620140047
179	Kakarvīši	385155	(Article)	2010	20180620140047
180	Kūzmi	385156	(Article)	1950	20180620140047
181	Piļcine	385157	(Article)	2004	20180620140047
182	Raibie	385158	(Article)	1948	20180620140047
183	Zuiči	385159	(Article)	1994	20180620140047
184	Černoste (Feimaņu pagasts)	385164	(Article)	2009	20180620140047
185	Ezergailīši	385165	(Article)	2017	20180620140047
186	Kovališki (Feimaņu pagasts)	385166	(Article)	2011	20180620140047
187	Krupeniški	385167	(Article)	2011	20180620140047
188	Leinakolns	385169	(Article)	1955	20180620140047
189	Dērvaniene	385175	(Article)	1966	20180620140047
190	Dziļāri	385176	(Article)	2012	20180620140047
191	Karitoni	385178	(Article)	2008	20180620140047
192	Kuderi	385181	(Article)	1977	20180620140047
193	Žogotas (Gaigalavas pagasts)	385186	(Article)	2009	20180620140047
194	Čudarāni	385191	(Article)	2025	20180620140047
195	Danči	385193	(Article)	1967	20180620140047
196	Īvoni	385199	(Article)	2049	20180620140047
197	Žogoti	385200	(Article)	2038	20180620140047
198	Kantinīki	385204	(Article)	1960	20180620140047
199	Leimaņi (Kantinieku pagasts)	385206	(Article)	2006	20180620140047
200	Pauri (Kantinieku pagasts)	385207	(Article)	2001	20180620140047
201	Batņi	385213	(Article)	1941	20180620140047
202	Kušneri (Kaunatas pagasts)	385214	(Article)	1949	20180620140047
203	Križini	385215	(Article)	1996	20180620140047
204	Ismeri	385216	(Article)	2036	20180620140047
205	Višķeri	385218	(Article)	2007	20180620140047
206	Bondari (Mākoņkalna pagasts)	396930	(Article)	2014	20180622210943
207	Dvarči	396931	(Article)	2054	20180622210943
208	Gineviči	396932	(Article)	2062	20180622210943
209	Jaunstašuļi	396933	(Article)	1985	20180622210943
210	Milka	396935	(Article)	1958	20180622210943
211	Škrjabi (Mākoņkalna pagasts)	396936	(Article)	2057	20180622210943
212	Stikuti	396940	(Article)	2014	20180622210943
213	Ubogova (Mākoņkalna pagasts)	396941	(Article)	1966	20180622210943
214	Vecstašuļi	398786	(Article)	1978	20180622210943
215	Zelenpole	398787	(Article)	2022	20180622210943
216	Zeļonki	398788	(Article)	2035	20180622211307
217	Lapatiški	398789	(Article)	2064	20180622212334
218	Leimaniški (Maltas pagasts)	398790	(Article)	2024	20180622212334
219	Īdeņa	398791	(Article)	2024	20180622213719
220	Zvejsola	398792	(Article)	1938	20180622213719
221	Brožgola	398793	(Article)	2004	20180622214844
"""

prop = 'P625'
wikiitem = 'Q728945'


repo = site.data_repository()



def getnames(namelistsss):
	namelistsss = namelistsss.split('\n')

	names = []

	for line in namelistsss:
		line = line.split('\t')
		if len(line)>1:
			line = line[1]
			#pywikibot.output(line)
			names.append(line)
	#pywikibot.output(names)
	return names
	
itemlist = getnames(listForWork)

def checkInstance(item):
	badinstances = ['Q5','Q783794','Q4167410','Q4830453','Q11879590','Q202444','Q12308941']
	
	claims = item.claims
	#pywikibot.output(claims)
	
	if not claims:
		return True
	
	if 'P279' in claims:
		return False
    
	if 'P31' in claims:
		for wdClaimValue in item.claims['P31']:
			if wdClaimValue.getTarget().title() in badinstances:
				print(wdClaimValue.getTarget().title())
				return False
				break
	
	return True
#
def one_item(article):
	page = pywikibot.Page(site,article)
	item = pywikibot.ItemPage.fromPage(page)
	oldcoordinate = page.coordinates(primary_only=True)
	
	if not oldcoordinate:
		return
		
	claims = item.get().get('claims')
	if prop in claims:
		pywikibot.output(u'Item %s already contains coordinates (%s)'
				 % (item.title(), prop))
		return
	
	bfds= []
	badprops = ['P247','P1282']
	for prop2 in badprops:
		if prop2 in claims:
			bfds.append(prop2)
			print('bad prop: ' + prop2 + ' - ' + item.title())
			#break
			return
		
	if len(bfds)>0:
		return
		
	checkinst = checkInstance(item)
	
	if not checkinst:
		print('bad instance, skipping: ' + item.title())
		return
	
	coord_lat = float(oldcoordinate.lat)
	coord_long = float(oldcoordinate.lon)
	precision = 0.00027777777777778#1/100000
	target = pywikibot.Coordinate(coord_lat, coord_long, precision=precision, globe_item='http://www.wikidata.org/entity/Q2')
	
	newclaim = pywikibot.Claim(repo, prop)
	newclaim.setTarget(target)
	pywikibot.output(u'Adding %s, %s to %s' % (coord_lat,
						   coord_long,
						   item.title()))
	try:
		item.addClaim(newclaim)
		importedEnWikipedia = pywikibot.Claim(repo, u'P143')
		enWikipedia = pywikibot.ItemPage(repo, wikiitem)
		importedEnWikipedia.setTarget(enWikipedia)
		newclaim.addSources([importedEnWikipedia])
	except CoordinateGlobeUnknownException as e:
		pywikibot.output(u'Skipping unsupported globe: %s' % e.args)
#
def main():
	for article in itemlist:
		one_item(article)
#
main()