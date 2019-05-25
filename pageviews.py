import gzip, pywikibot, os, sys

#/mnt/nfs/dumps-labstore1006.wikimedia.org/xmldatadumps/public/other/pageviews/2018/2018-05/
#os.chdir(r'projects/viewstats')

logfile = open('jun14-2018.txt','a', encoding='utf-8')

def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b


'''
with gzip.open('pageviews-20180501-000000.gz','r') as f:
	for line in f:
		line = encode_if_necessary(line).replace('\n','')
		if not line.startswith('lv'): continue
		if counter == 500: break
		counter += 1
		
		pywikibot.output(line)
'''
#
for r, d, f in os.walk(r'/mnt/nfs/dumps-labstore1006.wikimedia.org/xmldatadumps/public/other/pageviews/2018/2018-06/'):
	for file in f:
#for file in os.listdir(r'/mnt/nfs/dumps-labstore1006.wikimedia.org/xmldatadumps/public/other/pageviews/2018/2018-05/'):
		if 'pageviews-' not in file: continue
		
		if '20180614' not in file: continue
		fullname = os.path.join(r, file)
		with gzip.open(fullname,'r') as f:
			print(file)
			thisfiledata = []
			
			f_name = file.replace('pageviews-','').replace('.gz','')
			
			counter = 0
			for line in f:
				line = encode_if_necessary(line).replace('\n','')
				if not line.startswith('lv'): continue
				if counter % 5000 == 0:
					print(counter)
					sys.stdout.flush()
				counter += 1
				thisfiledata.append('{}\t{}'.format(f_name,line))
			
			logfile.write('{}\n'.format('\n'.join(thisfiledata)))