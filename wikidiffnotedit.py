import requests,json,lxml.html,time,sys,urllib,traceback,os,pywikibot
#from irccolour import colours
from bs4 import BeautifulSoup
#from colorama import Fore as colours
#from datetime import datetime
from re import search,DOTALL,sub
from bracketmatch import getmismatches
from datetime import date, datetime, timedelta, timezone

#os.chdir(r'projects/bracket')

ignore=["Sat-IP",]

sys.stdout.flush()
semiauto=False



def geteditwarning(page):
	nowarn=None
	'''
	for template, params in page.templatesWithParams():
		if template.lower()=="bots":
			for param in params:
				if param.strip()[:4]=="deny":
					for bot in param.partition("=")[2].split(","):
						if bot.lower()=="bracketbot":
							nowarn="Explicitly denied with {{bots}}"
						elif bot.lower()=="all":
							nowarn="Bots denied with {{bots}}"
				if param.strip()[:5]=="allow":
					for bot in param.partition("=")[2].split(","):
						if bot.lower()=="bracketbot":
							nowarn=None
		if template.lower()=="nobracketbot":
			nowarn="Explicitly denied with {{nobracketbot}}"
		if template.lower()=="dailybracketbot":
			nowarn=0
	for category in page.categories():
		if str(category)=='[[en:Category:Wikipedians who have opted out of BracketBot messages]]':
			nowarn="Explicitly denied with [[Category:Wikipedians who have opted out of BracketBot messages]]"
	'''
	return nowarn
#
def notifyMe(newtext):
	talkpage=pywikibot.Page(pywikibot.Site('lv', 'wikipedia'),"User talk:EdgarsBot")
	text=talkpage.get()
	talkpage.text = newtext
	talkpage.save(summary='Bot: Notice of potential markup breaking', botflag=False, minor=False)
#

def notify(user,diffid,title,reason,debug):
	if user=='Edgars2007':
		user='Experts'
	
	talkpage=pywikibot.Page(pywikibot.Site('lv', 'wikipedia'),"User talk:"+user)
	try:
		nowarn=geteditwarning(talkpage)
	except pywikibot.exceptions.IsRedirectPage:
		nowarn="User talk page is a redirect."
	if nowarn:
		print("Didn't notify "+user+" - "+nowarn)
		return
	try:
		nwe=True if nowarn==0 else False
		nowarn=geteditwarning(pywikibot.Page(pywikibot.Site('lv', 'wikipedia'),"User:"+user))
		if nowarn==None and nwe: nowarn=0
	except pywikibot.exceptions.IsRedirectPage:
		nowarn="User page is a redirect."
	if nowarn:
		print("Didn't notify "+user+" - "+nowarn)
		return
	remaining=getmismatches(pywikibot.Page(pywikibot.Site('lv', 'wikipedia'),title).get())
	if not remaining:
		print("Can't find any mismatches where there should be mismatches :/ Ignoring.")
		return
	try:
		text=talkpage.get()
	except pywikibot.exceptions.NoPage:
	#	if userlib.User(pywikibot.Site('lv', 'wikipedia'),user).isAnonymous():
	#		text="{{subst:Ipwelcome}} ~~~~\n"
	#	else:
	#		text="{{subst:welcome}} ~~~~\n"
		text = ""
	diffid = str(diffid)
	
		
	
	
	infotemp="\n{{subst:Iekavu paziņojums|diff=%s|page=%s|debug=%s|list=yes|remaining=%s|lines=%s}}" % (str(diffid), title, debug,remaining,remaining.count("\n"))
	#infotemp="\n\n{{"+"subst:User:BracketBot/inform|diff={diff}|page={page}|by={by}|debug={debug}|list=yes|remaining={remaining}".format(diff=diffid, page=title, by=reason, debug=debug, remaining=remaining)+"}}"
	header=("\n== Iekavas ("+datetime.strftime(datetime.now(),"%d.%m.%Y")+") ==") if nowarn==None else ("\n== Iekavas ("+datetime.strftime(datetime.now(),"%d.%m.%Y")+") ==")
	
	sectionstart=text.find(header)
	if sectionstart != -1:
		sectionend=text[sectionstart+len(header):].find("\n==")+sectionstart+len(header)
		if sectionend != sectionstart+len(header)-1:
			#insert template before sectionend
			newtext=text[:sectionend]+"\n"+infotemp+"\n"+text[sectionend:]
		else:
			#insert template at end
			newtext=text+"\n"+infotemp
	else:
		#create header
		newtext=text+header+"\n"+infotemp
	if semiauto==True:
		print("%About to notify {} for {} on http://en.wikipedia.org/w/index.php?diff={} Y/n?".format(user,debug,diffid))
		if raw_input()!="Y": return
	#talkpage.put_async(newtext,"Bot: Notice of potential markup breaking",minorEdit=False,callback=notenotified, botflag=False)
	
	if diffid in text:
		#notifyMe(newtext)
		return 0
	
	talkpage.text = newtext
	talkpage.save(summary='Bot: Notice of potential markup breaking', botflag=False, minor=False)
	
	
def notenotified(page,e):
	user=page.title()[page.title().find(":")+1:]
	if e is None:
		print("Notified "+user)
	else:
		print("Did not notify "+user+" "+str(e))
	sys.stdout.flush()

def matchbrackets(text):
	return text.count("(")-text.count(")"),text.count("[")-text.count("]"),text.count("{")-text.count("}"),text.count("<")-text.count(">")

def removeifwatching(title):
	global watch
	for diff in watch:
		if diff.title==title:
			print("%Removing {}".format(diff.title))
			watch.remove(diff)
			return

def printwatching():
	global watch
	t=[]
	for d in watch: t.append(d.title)
	print("%Watching: "+",".join(t))

def getpage(url):
	r = requests.get(url)
	r.encoding = 'utf-8'
	json_data = eval(r.text)
	
	return json_data

def enc(text):
	"""Yes a bodge function. Get over it."""
	try:
		return text.decode("utf-8")
	except UnicodeEncodeError:
		try:
			return text.encode("utf-8")
		except UnicodeEncodeError:
			return text

class Diff():
	def __init__(self):
		self.diffto=""
		self.difffrom=""
		self.bracketmatchold=""
		self.bracketmatchnew=""
		self.title=""
		self.user=""
		self.stamp=""
		self.pageid=0

checked=[]
watch=[]
origurl="http://lv.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvdiffto=prev&generator=recentchanges&grcnamespace=0&grclimit=20&grcshow=!bot&grctype=edit"
article="http://lv.wikipedia.org/w/api.php?action=parse&format=json&pageid="
rev="http://lv.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=sha1&rvlimit=50&pageids="

'''
https://phabricator.wikimedia.org/T97096
https://phabricator.wikimedia.org/T31223
'''
def one_loop(contin_old=''):
		global watch
		if contin_old!="":
			url = origurl + '?grccontinue='+contin_old
		else:
			url = origurl
		
		print(url)
		data=getpage(url)#get_api_fake()#getpage(url)
		
		contin = data["continue"]["grccontinue"]
		date_conti = contin.split('|')[0]
		contin_param = datetime.strptime(date_conti, '%Y%m%d%H%M%S')
		print('continue utc: '+date_conti)


		starp = (curr_time - contin_param).total_seconds()
		print('starp: '+str(starp))
		print('starpa2: '+str(starpa2))
		
		if starp>starpa2:
			need_more = False
		else:
			need_more = True
	
	
		for pageid in data["query"]["pages"]:
					try:
						if data["query"]["pages"][pageid]["revisions"][0]["diff"]["to"] in checked: continue
						#if data["query"]["pages"][pageid]["title"] in ignore: continue
						dtext=data["query"]["pages"][pageid]["revisions"][0]["diff"]["*"]
						#print("%{}".format(type(dtext)))
						#if type(dtext)!=unicode: continue
						diff = data["query"]["pages"][pageid]["revisions"][0]["diff"]["*"]
						#tree=lxml.html.fragments_fromstring(diff)
						tree = BeautifulSoup(diff, "html.parser")
						
						added = tree.find_all('td',{'class':"diff-addedline"})
						removed = tree.find_all('td',{'class':"diff-deletedline"})
						
						new = ''.join([f.text for f in added])
						old = ''.join([f.text for f in removed])
						
						mbo=matchbrackets(old)
						mbn=matchbrackets(new)
						if mbn==(0,0,0,0) or  matchbrackets(sub("\|name=.+?(?=[\|}])|<math>.+?<\/math>|<pre>.+?</pre>|\|title=.+?(?=[\|}])","",new))==(0,0,0,0):
							removeifwatching(data["query"]["pages"][pageid]["title"])
						comment=data["query"]["pages"][pageid]["revisions"][0]["comment"].lower()
						if comment.find("rv")+comment.find("revert")+comment.find("!nobot!")+3>0:
							removeifwatching(data["query"]["pages"][pageid]["title"])
							continue
						#print("%Scanning {} {} {}".format(data["query"]["pages"][pageid]["title"].encode('ascii','ignore'),mbo,mbn))
						if mbo==(0,0,0,0) and mbo != mbn:
							#print(data["query"]["pages"][pageid]["title"])
							d=Diff()
							d.diffto=data["query"]["pages"][pageid]["revisions"][0]["diff"]["to"]
							d.difffrom=data["query"]["pages"][pageid]["revisions"][0]["diff"]["from"]
							d.matchbracketold=mbo
							d.matchbracketnew=mbn
							d.title=data["query"]["pages"][pageid]["title"]
							d.user=data["query"]["pages"][pageid]["revisions"][0]["user"]
							d.stamp=datetime.now()
							d.pageid=pageid
							watch.append(d)
							pywikibot.output("%Adding {} {}".format(d.title, d.diffto))
							printwatching()
							checked.append(data["query"]["pages"][pageid]["revisions"][0]["diff"]["to"])
					except KeyError: pass
		return [need_more, contin]
#
#def one_res():
	

#3816
def fetchmismatches():
	global watch
	
	print('NEW BRACKETS!!!')
	need_more = True
	first_part = True
	
	lasttime = open("lasttime.log",'r').read()
	
	curr_time = datetime.utcnow()
	lasttime_obj = datetime.strptime(lasttime, '%Y%m%d%H%M%S')
	
	curr_log = curr_time.strftime('%Y%m%d%H%M%S')#start.strftime('%Y%m%d%H%M%S')
	
	starpa2 = (curr_time - lasttime_obj).total_seconds()
	lasttime_wr = open("lasttime.log",'w')
	lasttime_wr.write(curr_log)
	
	
	print('current utc: '+curr_log)
	print('last utc: '+lasttime)
	
	contin = ''
	while need_more:
		print('continpar: '+contin)
		if not first_part:
			url = origurl + '?grccontinue='+contin
		else:
			url = origurl
			first_part = False
		
		#print(url)
		data=getpage(url)#get_api_fake()#getpage(url)
		
		contin_new = data["continue"]["grccontinue"]
		
		if contin==contin_new:
			need_more = False
			
		
		contin = data["continue"]["grccontinue"]
		date_conti = contin.split('|')[0]
		contin_param = datetime.strptime(date_conti, '%Y%m%d%H%M%S')
		print('continue utc: '+date_conti)
	

		starp = (curr_time - contin_param).total_seconds()
		print('starp: '+str(starp))
		print('starpa2: '+str(starpa2))
		
		if starp>starpa2:
			need_more = False
	
	
		for pageid in data["query"]["pages"]:
					try:
						if data["query"]["pages"][pageid]["revisions"][0]["diff"]["to"] in checked: continue
						#if data["query"]["pages"][pageid]["title"] in ignore: continue
						dtext=data["query"]["pages"][pageid]["revisions"][0]["diff"]["*"]
						#print("%{}".format(type(dtext)))
						#if type(dtext)!=unicode: continue
						diff = data["query"]["pages"][pageid]["revisions"][0]["diff"]["*"]
						#tree=lxml.html.fragments_fromstring(diff)
						tree = BeautifulSoup(diff, "html.parser")
						
						added = tree.find_all('td',{'class':"diff-addedline"})
						removed = tree.find_all('td',{'class':"diff-deletedline"})
						
						new = ''.join([f.text for f in added])
						old = ''.join([f.text for f in removed])
						
						mbo=matchbrackets(old)
						mbn=matchbrackets(new)
						if mbn==(0,0,0,0) or  matchbrackets(sub("\|name=.+?(?=[\|}])|<math>.+?<\/math>|<pre>.+?</pre>|\|title=.+?(?=[\|}])","",new))==(0,0,0,0):
							removeifwatching(data["query"]["pages"][pageid]["title"])
						comment=data["query"]["pages"][pageid]["revisions"][0]["comment"].lower()
						if comment.find("rv")+comment.find("revert")+comment.find("!nobot!")+3>0:
							removeifwatching(data["query"]["pages"][pageid]["title"])
							continue
						#print("%Scanning {} {} {}".format(data["query"]["pages"][pageid]["title"].encode('ascii','ignore'),mbo,mbn))
						if mbo==(0,0,0,0) and mbo != mbn:
							#print(data["query"]["pages"][pageid]["title"])
							d=Diff()
							d.diffto=data["query"]["pages"][pageid]["revisions"][0]["diff"]["to"]
							d.difffrom=data["query"]["pages"][pageid]["revisions"][0]["diff"]["from"]
							d.matchbracketold=mbo
							d.matchbracketnew=mbn
							d.title=data["query"]["pages"][pageid]["title"]
							d.user=data["query"]["pages"][pageid]["revisions"][0]["user"]
							d.stamp=datetime.now()
							d.pageid=pageid
							watch.append(d)
							pywikibot.output("%Adding {} {}".format(d.title, d.diffto))
							printwatching()
							checked.append(data["query"]["pages"][pageid]["revisions"][0]["diff"]["to"])
					except KeyError: pass
	
#
#fetchmismatches()

if __name__=='__main__':
	#while 1:
		try:
			fetchmismatches()
			#printwatching()
			#while watch and (datetime.now()-watch[0].stamp).total_seconds()>600:
			print('checked')
			pywikibot.output(checked)
			print('watch')
			pywikibot.output(watch)
			for one in watch:
				foundmistake=watch.pop(0)
				#fp=getpage(article+foundmistake.pageid)
				data = getpage(article+foundmistake.pageid)
				#data=json.load(fp)
				dtext=data["parse"]["text"]["*"]
				if dtext.find("{{NoBracketBot}}")!=-1: continue
				dtext=sub("\|name=.+?(?=[\|}])|<math>.+?<\/math>|<pre>.+?</pre>|\|title=.+?(?=[\|}])","",dtext)
				if matchbrackets(dtext)==(0,0,0,0): continue
				if search(r'(?<!\d)1\)(.*)(?<!\d)2\)',dtext,DOTALL): continue
				if search(r'(?<!\w)a\)(.*)(?<!\w)b\)',dtext,DOTALL): continue
				#fp=getpage(rev+foundmistake.pageid)
				#revisions=json.load(fp)
				revisions = getpage(rev+foundmistake.pageid)
				first=True
				try:
					for rv in revisions["query"]["pages"][foundmistake.pageid]["revisions"]:
						if first:
							needle,first=rv["sha1"],False
						elif rv["sha1"]==needle: raise Exception("Sha not found")
				except (KeyError, Exception) as e:
					continue
				mb=foundmistake.matchbracketnew
				round="" if not mb[0] else (" "+str(abs(mb[0]))+" \"()\"s \r")
				square="" if not mb[1] else (" "+str(abs(mb[1]))+" \"[]\"s \r")
				curl="" if not mb[2] else (" "+str(abs(mb[2]))+" \"{}\"s \r")
				angle="" if not mb[3] else (" "+str(abs(mb[3]))+" \"<>\"s \r")
				repl="" if not sum(mb)==0 else " likely mistaking one for another"
				message=" by modifying "+(round+square+curl+angle).strip().replace("\r","and ")+repl
				#print(colours.light_cyan+"http://en.wikipedia.org/w/index.php?diff={}&oldid={}"+colours.clear+" "+colours.red+"{}"+colours.clear+" [["+colours.yellow+"{}"+colours.clear+"]] by \""+colours.dark_green+"{}"+colours.clear+"\" "+colours.orange+"{}").format(
				'''
				'print("http://en.wikipedia.org/w/index.php?diff={}&oldid={} {}  [[{}]] by \"{}\" {}").format(
				foundmistake.diffto,
				foundmistake.difffrom,
				foundmistake.matchbracketnew,
				foundmistake.title.encode('utf-8'),
				foundmistake.user.encode('utf-8'),
				enc(message)
				)
				'''
				
				checked=checked[-500:]#.remove(foundmistake.diffto)
				sys.stdout.flush()
				notify(foundmistake.user,foundmistake.diffto,foundmistake.title,message,foundmistake.matchbracketnew)
		except:
			print("Error, bailing out.")
			watch=[]
			checked=[]
			try:
				f=open("bracketbot.log",'a')
				f.write(traceback.format_exc()+"\n\n")
				f.close()
				print("Error logged.")
			except:
				print("Error while trying to log other error.")
								
		finally:
			sys.stdout.flush()
			#time.sleep(15)
