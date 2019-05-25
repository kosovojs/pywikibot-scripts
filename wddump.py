import bz2
import json
import sys
import time
import pywikibot

def main():
	wdsite = pywikibot.Site('wikidata', 'wikidata')
	p31 = {}
	c = 0
	t1 = time.time()
	gdfdfg = []
	dumpdate = '20180604'#sys.argv[1]
	f = bz2.open('/public/dumps/public/wikidatawiki/entities/%s/wikidata-%s-all.json.bz2' % (dumpdate, dumpdate), 'r')
	for line in f:
		line = line.decode('utf-8')
		#line = line.strip('\n').strip(',')
		c += 1
		if c==500: break
		gdfdfg.append(line)
	with open('dump.p31.txt', 'w') as f:
		f.write('\n'.join(gdfdfg))

if __name__ == '__main__':
	main()