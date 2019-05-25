#import MySQLdb as mysqldb
import toolforge
import json
import time
import sys
import codecs
from collections import defaultdict, OrderedDict
from datetime import datetime

begintime = time.time()
print('Begin: {}'.format(begintime))

alreadydone = """
itwikibooks
afwikiquote
srnwiki
jamwiki
snwiki
dawikibooks
azbwiki
mswiki
enwikiversity
sdwiki
rmywiki
simplewiki
zawiki
iswiki
commonswiki
xhwiki
ruwikiversity
kvwiki
plwikibooks
zhwikiquote
aswiki
ptwikiquote
mywiki
srwikiquote
nlwikisource
thwikiquote
slwiki
lnwiki
ladwiki
jawikiversity
arwiki
iswikibooks
afwiki
trwikiquote
vewiki
crhwiki
elwikivoyage
itwikiversity
tawikibooks
nnwiki
fawikiquote
kaawiki
eowikiquote
gdwiki
angwiki
cuwiki
kgwiki
newwiki
viwikibooks
fiwikinews
roa_tarawiki
tiwiki
ptwiki
dewiktionary
tswiki
amwiki
iswikiquote
iuwiki
siwiki
csbwiki
mnwiki
hiwiki
elwiki
fawikibooks
jawikisource
gvwiki
cswikisource
pamwiki
olowiki
brwiki
hywikiquote
kshwiki
quwiki
ganwiki
cswikibooks
krcwiki
nnwikiquote
furwiki
hewikivoyage
tnwiki
guwikiquote
ukwiki
viwikiquote
itwikivoyage
klwiki
bmwiki
be_x_oldwiki
bclwiki
sowiki
glwikiquote
bgwiki
azwikibooks
jawikibooks
elwikibooks
kawiki
dewikinews
arwikiquote
uzwikiquote
vecwiki
nahwiki
hewikinews
mznwiki
liwikiquote
arwikisource
acewiki
rowikiquote
ndswiki
xmfwiki
nvwiki
fiwikivoyage
bswiki
ltwikiquote
nrmwiki
fowiki
frwiktionary
nlwikinews
fiu_vrowiki
elwikinews
dtywiki
nawiki
cswikiquote
srwiki
hawwiki
huwikibooks
cawikisource
tewiki
lmowiki
bawiki
kywiki
omwiki
zh_yuewiki
kswiki
nowiki
chrwiki
simplewikiquote
map_bmswiki
itwikinews
thwikibooks
kbdwiki
kowiki
biwiki
huwiki
ruwikibooks
nsowiki
slwikisource
ptwikibooks
hrwikiquote
fjwiki
xalwiki
minwiki
chwiki
ptwikisource
bat_smgwiki
enwikivoyage
tpiwiki
bswikiquote
tlwiki
plwikisource
mrjwiki
vlswiki
vepwiki
euwikiquote
tywiki
rmwiki
hiwikibooks
enwikinews
jawikiquote
jbowiki
jawikinews
ckbwiki
tumwiki
fawikinews
szlwiki
htwiki
orwiki
extwiki
emlwiki
iewiki
frrwiki
fiwiki
dewikiversity
sawiki
iowiki
cebwiki
napwiki
bgwikiquote
zhwikibooks
cswiki
gomwiki
lijwiki
towiki
ruwikinews
hsbwiki
scnwiki
brwikiquote
cawikiquote
scowiki
mrwiki
zhwikivoyage
glwiki
azwikisource
nlwikibooks
ukwikisource
dawikiquote
ikwiki
warwiki
kiwiki
bxrwiki
astwiki
frwikisource
plwiki
dinwiki
eswikiversity
nowikibooks
bnwiki
etwiki
skwikiquote
enwikisource
bgwikisource
yiwiki
dvwiki
idwikisource
tcywiki
svwikiquote
uzwiki
enwiki
"""
#
alreadydone = [f for f in alreadydone.split('\n') if len(f)>3]
#have to do enwiki!

order = '''enwiki	32262
dewiki	9762
arwiki	8686
frwiki	8529
eswiki	7889
itwiki	7112
plwiki	6762
ptwiki	6465
ruwiki	6210
jawiki	5217
nlwiki	5015
fawiki	5007
zhwiki	4537
svwiki	4378
cawiki	3801
commonswiki	3781
ukwiki	3619
srwiki	3397
fiwiki	3355
hewiki	3065
cswiki	2885
kowiki	2716
shwiki	2621
nowiki	2495
trwiki	2386
idwiki	2207
thwiki	1866
huwiki	1829
dawiki	1826
simplewiki	1825
rowiki	1687
slwiki	1625
hrwiki	1545
viwiki	1522
glwiki	1492
bgwiki	1477
etwiki	1437
euwiki	1410
eowiki	1378
elwiki	1251
hiwiki	1236
hywiki	1225
tawiki	1202
ltwiki	1129
cywiki	1129
skwiki	1114
kkwiki	1108
gawiki	1025
azbwiki	974
orwiki	922
mswiki	917
bewiki	902
azwiki	891
lvwiki	798
mkwiki	796
mlwiki	782
bswiki	782
lawiki	731
nnwiki	711
kywiki	640
tlwiki	632
bnwiki	620
urwiki	611
zh_yuewiki	606
uzwiki	580
tewiki	567
iswiki	566
kawiki	564
afwiki	529
astwiki	486
iowiki	480
scowiki	477
be_x_oldwiki	393
itwikiquote	392
sqwiki	383
knwiki	369
ckbwiki	350
pawiki	325
swwiki	324
zh_min_nanwiki	317
dvwiki	300
warwiki	291
siwiki	288
mrwiki	285
jvwiki	285
ocwiki	281
specieswiki	269
mywiki	256
ttwiki	237
newiki	232
enwikiquote	213
pswiki	209
lbwiki	209
yiwiki	207
fywiki	206
kuwiki	205
plwikiquote	203
quwiki	199
newwiki	191
brwiki	188
tgwiki	185
iawiki	183
scnwiki	180
suwiki	169
pnbwiki	166
wawiki	165
ndswiki	162
enwikisource	161
alswiki	149
mnwiki	142
arzwiki	135
htwiki	130
aswiki	118
yowiki	118
guwiki	114
anwiki	108
bawiki	106
dewikiquote	105
sawiki	104
liwiki	103
emlwiki	100
cebwiki	97
lnwiki	94
eswikiquote	90
sahwiki	87
lmowiki	81
sowiki	79
gdwiki	78
frwikiquote	78
bat_smgwiki	77
mgwiki	76
diqwiki	75
skwikiquote	73
gnwiki	72
fowiki	71
jamwiki	71
wuuwiki	70
barwiki	67
frwikiversity	66
cvwiki	64
ptwikiquote	64
sdwiki	62
xmfwiki	61
amwiki	59
ruwikinews	59
cswikiquote	59
tkwiki	58
zh_classicalwiki	57
ruwikiquote	56
cdowiki	55
pmswiki	55
ukwikiquote	54
hakwiki	52
snwiki	49
eowikiquote	48
scwiki	48
itwikisource	48
pamwiki	47
ilowiki	46
mznwiki	45
ruewiki	45
elwikiquote	44
bowiki	43
csbwiki	43
dewikisource	43
bswikiquote	43
bxrwiki	42
zawiki	42
ltwikiquote	41
fiu_vrowiki	41
lgwiki	40
cawikiquote	40
hewikiquote	39
trwikiquote	39
lijwiki	36
frrwiki	36
fawikiquote	35
hifwiki	35
slwikiquote	33
aywiki	33
tyvwiki	32
hrwikiquote	32
itwikiversity	32
omwiki	32
maiwiki	31
bgwikiquote	31
vecwiki	31
kmwiki	30
xhwiki	30
piwiki	29
rwwiki	29
frwikisource	29
ganwiki	28
bjnwiki	28
arcwiki	27
mwlwiki	27
bclwiki	26
gvwiki	26
frwikivoyage	25
szlwiki	25
kbpwiki	25
enwikinews	25
sewiki	25
enwikivoyage	24
extwiki	24
nds_nlwiki	24
igwiki	23
bhwiki	23
vepwiki	23
enwikiversity	23
roa_rupwiki	22
fiwikiquote	21
mtwiki	21
eowikinews	21
vlswiki	21
dtywiki	20
kshwiki	20
nahwiki	20
dewikinews	20
iuwiki	19
chrwiki	19
hywikiquote	19
oswiki	19
jbowiki	19
furwiki	19
enwikibooks	19
dewikibooks	19
lowiki	18
gomwiki	18
lezwiki	18
napwiki	18
lawikiquote	18
rnwiki	18
azwikiquote	18
tiwiki	17
ugwiki	17
nlwikinews	17
dinwiki	17
arwikiversity	16
cowiki	16
frwikinews	16
etwikiquote	15
nsowiki	15
akwiki	15
sswiki	15
nywiki	15
nnwikiquote	15
jawikiquote	14
hawiki	14
tswiki	14
angwiki	14
huwikiquote	14
kaawiki	14
zhwikiquote	13
jawikibooks	13
cewiki	13
acewiki	13
stqwiki	13
stwiki	13
minwiki	13
frwikibooks	13
mrjwiki	12
papwiki	12
eswikiversity	12
tcywiki	11
arwikiquote	11
mhrwiki	11
lbewiki	11
vowiki	11
nrmwiki	11
novwiki	11
nvwiki	11
nlwikiquote	10
hsbwiki	10
bmwiki	10
bpywiki	9
srwikiquote	9
kvwiki	9
avwiki	9
itwikibooks	9
eswikinews	9
cswikisource	9
liwikiquote	9
kowikiquote	8
koiwiki	8
myvwiki	8
ruwikisource	8
ruwikibooks	8
kiwiki	8
kabwiki	8
zeawiki	8
wowiki	8
zuwiki	8
eswikibooks	8
iewiki	8
tnwiki	8
urwikiquote	7
arwikibooks	7
hewikivoyage	7
rowikiquote	7
olowiki	7
map_bmswiki	7
ladwiki	7
pdcwiki	7
svwikiquote	7
eswikisource	7
zhwikivoyage	6
arwikinews	6
lrcwiki	6
udmwiki	6
xalwiki	6
chywiki	6
ikwiki	6
eewiki	6
nowikiquote	6
ptwikinews	6
hawwiki	6
zhwikibooks	5
kawikiquote	5
mdfwiki	5
krcwiki	5
thwikibooks	5
biwiki	5
iswikibooks	5
dewikivoyage	5
pcdwiki	5
kuwikiquote	5
frpwiki	5
svwikinews	5
nlwikibooks	5
itwikinews	5
kwwiki	5
thwikiquote	4
arwikisource	4
glkwiki	4
klwiki	4
srnwiki	4
miwiki	4
dawikiquote	4
rowikibooks	4
cbk_zamwiki	4
fiwikivoyage	4
euwikiquote	4
svwikivoyage	4
ptwikibooks	4
roa_tarawiki	4
ptwikisource	4
kowikinews	3
zhwikinews	3
tewikiquote	3
tawikiquote	3
hiwikibooks	3
fawikibooks	3
kbdwiki	3
abwiki	3
elwikisource	3
slwikisource	3
cywikiquote	3
pflwiki	3
glwikiquote	3
trwikinews	3
ptwikivoyage	3
rmywiki	3
iswikiquote	3
rowikisource	3
gotwiki	2
jawikisource	2
zhwikisource	2
jawikinews	2
mlwikiquote	2
tawikibooks	2
kswiki	2
fawikisource	2
hewikisource	2
bgwikisource	2
ruwikiversity	2
srwikinews	2
srwikibooks	2
azwikibooks	2
simplewikiquote	2
metawiki	2
huwikibooks	2
vewiki	2
svwikibooks	2
itwikivoyage	2
tpiwiki	2
pihwiki	2
pagwiki	2
rmwiki	2
uzwikiquote	2
atjwiki	2
viwikiquote	2
dewikiversity	2
towiki	2
nowikinews	2
kgwiki	2
lawikisource	2
nlwikivoyage	2
fiwikibooks	2
nawiki	2
plwikibooks	2
cawikinews	2
nlwikisource	2
afwikiquote	2
kowikisource	1
jawikiversity	1
dzwiki	1
thwikisource	1
tawikinews	1
tawikisource	1
guwikiquote	1
bnwikisource	1
hiwikiquote	1
fawikinews	1
fawikivoyage	1
hewikinews	1
ukwikisource	1
cuwiki	1
bgwikinews	1
mkwikibooks	1
srwikisource	1
ruwikivoyage	1
bewikiquote	1
elwikivoyage	1
elwikibooks	1
elwikinews	1
plwiktionary	1
enwiktionary	1
frwiktionary	1
fjwiki	1
wikidatawiki	1
viwikisource	1
dewiktionary	1
viwikibooks	1
dsbwiki	1
cswikibooks	1
eowikibooks	1
azwikisource	1
brwikiquote	1
fiwikinews	1
lawikibooks	1
crhwiki	1
chwiki	1
sqwikiquote	1
tetwiki	1
trwikisource	1
tywiki	1
huwikinews	1
cswikinews	1
idwikisource	1
dawikibooks	1
nowikibooks	1
smwiki	1
glwikibooks	1
cawikibooks	1
gagwiki	1
ffwiki	1
slwikibooks	1
plwikivoyage	1
plwikisource	1
cawikisource	1
tumwiki	1'''
order = [f.split('\t')[0] for f in order.split('\n') if len(f)>3][::-1]

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]
#

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

wikis = eval(open('wdapidfsdfRES-test.txt', 'r', encoding='utf-8').read())

res = {}

filesave = open('ffsdffgggdffsdfsdfsdgddfsd-fina0-212121.txt', 'a', encoding='utf-8')

for wiki in order:
	counter = 0
	#if wiki in alreadydone: continue
	
	if wiki not in wikis: continue
	
	if wiki=='commonswiki': continue
	
	print(wiki)
	print(str(datetime.now()))
	sys.stdout.flush()
	#conn = mysqldb.connect(wiki.replace('-','_') + ".labsdb", db= wiki.replace('-','_') + '_p',
	#						   read_default_file="~/replica.my.cnf")
	conn = toolforge.connect(wiki.replace('-','_') + '_p')
	for chunk in chunks(wikis[wiki], 100):
		
		chunk = [i.replace("'", "\\'").replace(' ','_') for i in chunk]
		query = "select page_id from page where page_namespace=0 and page_title in ('" + "','".join(chunk) + "');"
		query = query.encode('utf-8')
		#print(query)
		try:
			cursor = conn.cursor()
			cursor.execute(query)
			rows = cursor.fetchall()
		except KeyboardInterrupt:
			sys.exit()
		revids = []
		for row in rows:
			revids.append(str(int(row[0])))
		if not revids:
			counter += 1
			continue
		query = "select rev_user_text, count(*) as count from revision where rev_page in (" + ",".join(revids) + ") and rev_timestamp like '2017%' group by rev_user_text;"
		try:
			cursor = conn.cursor()
			#print('Exec query ' + query)
			#print(counter)
			query = query.encode('utf-8')
			cursor.execute(query)
			rows = cursor.fetchall()
		except KeyboardInterrupt:
			sys.exit()
		thischunksave = []
		for row in rows:
			user = encode_if_necessary(row[0])
			editc = row[1]
			
			thischunksave.append('\t'.join([wiki,str(user),str(editc)]))
		filesave.write('\n'.join(thischunksave)+'\n')
			
		#res_wikis.append(wiki + str(counter))
		#with codecs.open('ffsdfdfsd.json', 'w', 'utf-8') as f:
		#	f.write(str(res))
		#with codecs.open('ffsdfdsfsdfsdfsdfdfsd.json', 'w', 'utf-8') as f:
		#	f.write(json.dumps(res_wikis))
		counter += 1
#
print('done!')
endtime = time.time()
print('End: {}, took so much: {}'.format(endtime,(endtime-begintime)))
sys.stdout.flush()