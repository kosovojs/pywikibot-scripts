#!/usr/bin/python
# -*- coding: utf-8  -*-
import re, os, sys, pywikibot, toolforge
from glob import glob

connLabs = toolforge.connect_tools('s53143__meta_p')
cursor1 = connLabs.cursor()

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(query,connection = connLabs):
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

def getLastDump(jobName='dumpsGeneral'):
	if jobName=='':
		query = "select min(updateString) from logtable where job like 'dumps%'"
		query_res = run_query(query,connLabs)
	else:
		query = "select updateString from logtable where job='{}'".format(jobName)
		query_res = run_query(query,connLabs)
	
	return int(encode_if_necessary(query_res[0][0]))

def setLastDump(updated,jobName='dumpsGeneral'):
	query = "UPDATE `logtable` SET updateString=%s where job=%s"
	
	cursor1.execute(query, (updated, jobName))
	connLabs.commit()

def getLastFile(wantedfile = "articlesdump", thelastchecked = '', jobname='dumpsGeneral'):
	names = [os.path.basename(re.sub('/$','',x)) for x in glob("/public/dumps/public/lvwiki/*/") if 'latest' not in x]
	subfolder = int(max(sorted(names, key=lambda x: int(x))))
	#pywikibot.output(subfolder)
	
	if thelastchecked=='':
		thelastchecked = getLastDump(jobname)
	
	thelastchecked = int(thelastchecked)
	
	if subfolder<=thelastchecked:
		#print('not yet')
		return False
	#
	thepath = '/public/dumps/public/lvwiki/{}/'.format(subfolder)
	
	statusfile = eval(open("{}dumpstatus.json".format(thepath), "r", encoding='utf-8').read())["jobs"]
	
	if wantedfile in statusfile and statusfile[wantedfile]['status']=='done':
		filename = list(statusfile[wantedfile]['files'].keys())[0]
		fullpath = "{}{}".format(thepath,filename)
		#print(fullpath)
		return {'path':fullpath,'date':subfolder}
	
	return False
#
#getLastFile()

def checkLastFile(wantedfile = "articlesdump", thelastchecked = ''):
	names = [os.path.basename(re.sub('/$','',x)) for x in glob("/public/dumps/public/lvwiki/*/") if 'latest' not in x]
	subfolder = int(max(sorted(names, key=lambda x: int(x))))
	pywikibot.output(subfolder)
	
	if thelastchecked=='':
		thelastchecked = getLastDump("")
	
	thelastchecked = int(thelastchecked)
	
	if subfolder<=thelastchecked:
		return 1
	#
	thepath = '/public/dumps/public/lvwiki/{}/'.format(subfolder)
	
	statusfile = eval(open("{}dumpstatus.json".format(thepath), "r", encoding='utf-8').read())["jobs"]
	
	if wantedfile in statusfile and statusfile[wantedfile]['status']=='done':
		print(statusfile[wantedfile])
		return 0
		
	return 1
#

if __name__ == '__main__':
	isOK = checkLastFile()
	sys.exit(isOK)
#else:
#	print('from other script')