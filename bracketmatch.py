# -*- coding: utf-8 -*-
import cgi, re
MISMATCH_DISTANCE=100
def getmismatches(text):
	rs,ss,cs,ns,ae=[],[],[],[],[]
	for i in range(len(text)):
		ch=text[i]
		if ch=='(': rs.append(i)
		elif ch=='[': ss.append(i)
		elif ch=='{': cs.append(i)
		elif ch=='<': ns.append(i)
		try:
			if ch==')': rs.pop()
			elif ch==']': ss.pop()
			elif ch=='}': cs.pop()
			elif ch=='>': ns.pop()
		except IndexError:
			ae.append(i)
	mismatches=[]
	mismatches.extend(rs)
	mismatches.extend(ss)
	mismatches.extend(cs)
	mismatches.extend(ns)
	mismatches.extend(ae)
	mismatches.sort()
	ret=""
	while mismatches:
		highlighted,started=False,False
		i=mismatches[0]-MISMATCH_DISTANCE
		if i<0: i=0
		cur="<p>"
		mismatches,ret,cur,i,highlighted,started=_getnextmismatch(text,mismatches,ret,cur,i,highlighted,started)
	#
	#if ret.startswith(['[[','{{']):
	
	if ret.endswith(('[[','{{')):
		ret = re.sub(r'[\[\{]{2}$',r'',ret)
		
	if ret.startswith(('}}',']]')):
		ret = re.sub(r'^[\]\}]{2}',r'',ret)
		
	return ret or "None"

pre='<span style="color:red;font-weight:bold;">'
post="</span>"
def _getnextmismatch(text,mismatches,ret,cur,i,highlighted,started):
	while i<len(text):
		ch=text[i]
		if ch=="\n":
			if highlighted:
				cur+=cgi.escape(ch)
				break
			else:
				cur=""
		elif len(mismatches)>1 and i==mismatches[1]:
			mismatches.pop(0)
			cur+=pre+"&#"+str(ord(ch))+";"+post
		elif i==mismatches[0]:
			cur+=pre+"&#"+str(ord(ch))+";"+post
			highlighted=True
		else:
			if started:
				cur+=cgi.escape(ch)
			elif not ch.isalnum():
				started=True
		if i==mismatches[0]+MISMATCH_DISTANCE:
			break
		i+=1
	cur=cur.replace(post+pre,"")
	while cur[-1].isalnum():
		cur=cur[:-1]
	ret+=cur.strip()+""
	mismatches.pop(0)
	return mismatches,ret,cur,i,highlighted,started
