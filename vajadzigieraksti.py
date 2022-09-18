import re, pywikibot, sys
from datetime import datetime
import toolforge

site = pywikibot.Site("lv", "wikipedia")
conn = toolforge.connect('lvwiki_p','analytics')
#apvienot ar Vikiprojekts:Vikipēdijas uzlabošana/Raksti/Pieprasītās lapas

SQL = """select pl_title,c
from (select pl_title , count(*) as c , pl_namespace
      from pagelinks
      where pl_from_namespace=0 and pl_namespace=0
      group by pl_title, pl_namespace
      having count(*)>10) as pl
  left join page
    on (pl_title=page_title and page_namespace= pl_namespace)
where page_id is null
order by c desc"""

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
quaryrun = run_query()

page_prefix = 'Vikipēdija:Vajadzīgie raksti/Visas sarkanās saites'

info_pretext = """* Avots: [[quarry:query/{source}]]
* Atjaunināšanas brīdis: {update}"""

info_header = '<!-- INFO START -->'
info_footer = '<!-- INFO END -->'

list_header = '<!-- LIST START -->'
list_footer = '<!-- LIST END -->'

def makeupdate(date):
	from datetime import datetime
	mon = {
		'1':'janvāris',
		'2':'februāris',
		'3':'marts',
		'4':'aprīlis',
		'5':'maijs',
		'6':'jūnijā',
		'7':'jūlijs',
		'8':'augusts',
		'9':'septembris',
		'10':'oktobris',
		'11':'novembris',
		'12':'decembris'
	}
	f = "%Y-%m-%dT%H:%M:%S"
	datetime = date
	#print(datetime.timetuple())
	#http://stackoverflow.com/questions/17118071/python-add-leading-zeroes-using-str-format

	dateee = "{}. gada {}. {} plkst. {:0>2}:{:0>2}:{:0>2}".format(datetime.year,datetime.day,mon[str(datetime.month)],datetime.hour,datetime.minute,datetime.second)

	return dateee
#
dateget = makeupdate(datetime.now())

def doreplace(text,pretext,header,footer):
	newtext = re.sub(header + '.*' + footer, header + '\n' + pretext + '\n' + footer, text, flags=re.DOTALL)
	#pywikibot.output(newtext)

	return newtext
#
def infotext(lvwikipagetext,source,number,old,upddate=dateget):
	info_pretext2 = info_pretext.format(source=source,update=dateget)
	newtext = doreplace(lvwikipagetext,info_pretext2,info_header,info_footer)

	return newtext

#raksti ar visv izmantotie aizs att
def main():
	#data = getdata('1')
	data = quaryrun
	oldquery = '16153'
	page = pywikibot.Page(site,page_prefix)
	text = page.get()
	countinst = len(data)
	thistext = infotext(text,oldquery,countinst,oldquery)

	report = []
	#vispirms jasakarto
	for articles in data[:3000]:
		articles = [encode_if_necessary(f) for f in articles]
		lv = articles[0].replace('_',' ')
		row = "|-\n| [[{}]] || {}".format(lv,articles[1])
		report.append(row)

	#pywikibot.output(report)

	header = '{| class="sortable wikitable"\n|-\n! Lapa !! Saites'
	table = '\n'.join(report)
	end = '|}'

	finalout = header+'\n'+table+'\n'+end

	thistext = doreplace(thistext,finalout,list_header,list_footer)
	page.text = thistext
	page.save(summary="Bots: atjaunināts", botflag=False, minor=False)

	return countinst
#
main()
