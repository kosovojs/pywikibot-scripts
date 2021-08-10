def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def get_label(data, fallback):
	if len(data) ==0:
		return None

	for lang in fallback:
		if not lang.endswith('wiki'):
			lang = '{}wiki'.format(lang)
		if lang in data:
			return data.get(lang), lang

	lang = list(data)[0]
	return data.get(lang), lang

def clean_api(claim_data):
	toret = {}

	for prop in claim_data:
		if prop=='P1087': continue#elo rangs
		thisprop = claim_data.get(prop)

		theseclaims = []

		for claim in thisprop:
			datatype = claim['mainsnak']['datatype']
			claimtosave = None
			if 'datavalue' in claim['mainsnak']:

				if datatype in ('external-id','string','commonsMedia','url'):
					claimtosave = claim['mainsnak']['datavalue']['value']
				elif datatype=='wikibase-item':
					claimtosave = claim['mainsnak']['datavalue']['value']['id']
				elif datatype=='time':
					claimtosave = claim['mainsnak']['datavalue']['value']['time']+'/'+str(claim['mainsnak']['datavalue']['value']['precision'])
				elif datatype=='quantity':
					claimtosave = claim['mainsnak']['datavalue']['value']['amount']+'U'+str(claim['mainsnak']['datavalue']['value']['unit'].replace('http://www.wikidata.org/entity/Q',''))
				elif datatype=='monolingualtext':
					claimtosave = claim['mainsnak']['datavalue']['value']['language']+': '+claim['mainsnak']['datavalue']['value']['text']
				else:
					print(prop, datatype)

				if claimtosave:
					theseclaims.append(claimtosave)
		toret[prop] = theseclaims

	return toret
#

wplist = set(["abwiki", "acewiki", "adywiki", "afwiki", "akwiki", "amwiki", "anwiki", "angwiki", "arwiki", "arcwiki", "arzwiki", "aswiki", "astwiki", "atjwiki", "avwiki", "aywiki", "azwiki", "azbwiki", "bawiki", "barwiki", "bclwiki", "bewiki", "be_x_oldwiki", "bgwiki", "bhwiki", "biwiki", "bjnwiki", "bmwiki", "bnwiki", "bowiki", "bpywiki", "brwiki", "bswiki", "bugwiki", "bxrwiki", "cawiki", "cbk_zamwiki", "cdowiki", "cewiki", "cebwiki", "chwiki", "chrwiki", "chywiki", "ckbwiki", "cowiki", "crwiki", "crhwiki", "cswiki", "csbwiki", "cuwiki", "cvwiki", "cywiki", "dawiki", "dewiki", "dinwiki", "diqwiki", "dsbwiki", "dtywiki", "dvwiki", "dzwiki", "eewiki", "elwiki", "emlwiki", "enwiki", "testwiki", "test2wiki", "simplewiki", "eowiki", "eswiki", "etwiki", "euwiki", "extwiki", "fawiki", "ffwiki", "fiwiki", "fjwiki", "fowiki", "frwiki", "frpwiki", "frrwiki", "furwiki", "fywiki", "gawiki", "gagwiki", "ganwiki", "gdwiki", "glwiki", "glkwiki", "gnwiki", "gomwiki", "gorwiki", "gotwiki", "alswiki", "guwiki", "gvwiki", "hawiki", "hakwiki", "hawwiki", "hewiki", "hiwiki", "hifwiki", "hrwiki", "hsbwiki", "htwiki", "huwiki", "hywiki", "iawiki", "idwiki", "iewiki", "igwiki", "ikwiki", "ilowiki", "inhwiki", "iowiki", "iswiki", "itwiki", "iuwiki", "jawiki", "jamwiki", "jbowiki", "jvwiki", "kawiki", "kaawiki", "kabwiki", "kbdwiki", "kbpwiki", "kgwiki", "kiwiki", "kkwiki", "klwiki", "kmwiki", "knwiki", "kowiki", "koiwiki", "krcwiki", "kswiki", "kshwiki", "kuwiki", "kvwiki", "kwwiki", "kywiki", "lawiki", "ladwiki", "lbwiki", "lbewiki", "lezwiki", "lfnwiki", "lgwiki", "liwiki", "lijwiki", "lmowiki", "lnwiki", "lowiki", "lrcwiki", "ltwiki", "ltgwiki", "lvwiki", "zh_classicalwiki", "maiwiki", "map_bmswiki", "mdfwiki", "mgwiki", "mhrwiki", "miwiki", "minwiki", "mkwiki", "mlwiki", "mnwiki", "mrwiki", "mrjwiki", "mswiki", "mtwiki", "mwlwiki", "mywiki", "myvwiki", "mznwiki", "nawiki", "nahwiki", "zh_min_nanwiki", "napwiki", "nowiki", "ndswiki", "nds_nlwiki", "newiki", "newwiki", "nlwiki", "nnwiki", "novwiki", "nrmwiki", "nsowiki", "nvwiki", "nywiki", "ocwiki", "olowiki", "omwiki", "orwiki", "oswiki", "pawiki", "pagwiki", "pamwiki", "papwiki", "pcdwiki", "pdcwiki", "pflwiki", "piwiki", "pihwiki", "plwiki", "pmswiki", "pnbwiki", "pntwiki", "pswiki", "ptwiki", "quwiki", "rmwiki", "rmywiki", "rnwiki", "rowiki", "roa_tarawiki", "ruwiki", "ruewiki", "roa_rupwiki", "rwwiki", "sawiki", "sahwiki", "scwiki", "scnwiki", "scowiki", "sdwiki", "sewiki", "sgwiki", "bat_smgwiki", "shwiki", "siwiki", "skwiki", "slwiki", "smwiki", "snwiki", "sowiki", "sqwiki", "srwiki", "srnwiki", "sswiki", "stwiki", "stqwiki", "suwiki", "svwiki", "swwiki", "szlwiki", "tawiki", "tcywiki", "tewiki", "tetwiki", "tgwiki", "thwiki", "tiwiki", "tkwiki", "tlwiki", "tnwiki", "towiki", "tpiwiki", "trwiki", "tswiki", "ttwiki", "tumwiki", "twwiki", "tywiki", "tyvwiki", "udmwiki", "ugwiki", "ukwiki", "urwiki", "uzwiki", "vewiki", "vecwiki", "vepwiki", "viwiki", "vlswiki", "vowiki", "fiu_vrowiki", "wawiki", "warwiki", "wowiki", "wuuwiki", "xalwiki", "xhwiki", "xmfwiki", "yiwiki", "yowiki", "zh_yuewiki", "zawiki", "zeawiki", "zhwiki", "zuwiki"])
