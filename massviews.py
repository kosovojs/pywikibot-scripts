import bz2, os
import sys, pywikibot, os, re
import json
import sys
import time
import pywikibot
import gzip
import heapq

null = ''

#os.chdir(r'projects/latvija')

#{"data":[3,2,1,3,3,5,4,5,11,5,2,8,4,103,197,176,224,309,266,149,349,685],"label":"Lāčplēša diena","project":"lv.wikipedia.org","sum":96400, "average":78.75816993464052,"index":1800}

bigfile = {}

def mean123(numbers):
	return (sum(numbers, 0.0))/(len(numbers))#float(sum(numbers)) / max(len(numbers), 1)
#
#http://stevehanov.ca/blog/index.php?id=122
def heapSearch( bigArray, k ):
	heap = []
	# Note: below is for illustration. It can be replaced by 
	# heapq.nlargest( bigArray, k )
	for item in bigArray:
		# If we have not yet found k items, or the current item is larger than
		# the smallest item on the heap,
		if len(heap) < k or item > heap[0]:
			# If the heap is full, remove the smallest element on the heap.
			if len(heap) == k: heapq.heappop( heap )
			# add the current element as the new smallest.
			heapq.heappush( heap, item )
	return heap
#
def one_file(filename):
	print(filename)
	petscan = eval(open(filename, "r", encoding='utf-8').read())
	print('did read')
	counter = 0
	for entry in petscan:
		counter += 1
		if counter % 250 == 0:
			print(counter)
		#wiki,article,str(sum(dict1)),str(len(dict1)),str('|'.join(joined))
		#entitle,wiki,article,summa,_,alldata = entry
		title = entry['label']
		data = entry['data']
		
		#try:
		data = [int(f) for f in data if isinstance(f,int)]
		try:
			mean1 = mean123(data)
			meancheck = 3*mean1
			newdata = [f for f in data if f<meancheck]
			newmean = mean123(newdata)
			dataForMean2 = data[-30:]
			newmean2 = mean123(dataForMean2)
			
		except:
			print(data)
		
		
		
		#if newmean2>2:
		toadd = ["{0:.2f}".format(mean1),"{0:.2f}".format(newmean2),sum(data),sum(dataForMean2)]
		bigfile.update({title:toadd})
#

json_files = [pos_json for pos_json in os.listdir() if pos_json.endswith('.json') and 'massviews-' in pos_json]
print(json_files)

for ziparchive in json_files:
	one_file(ziparchive)
	
with open('skatijumi.txt', "w", encoding='utf-8') as toSave:
	toSave.write(str(bigfile))
#
print(len(bigfile))