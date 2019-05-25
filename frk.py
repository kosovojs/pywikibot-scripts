import pywikibot, os
#os.chdir(r'projects/cee')

fileeopen = eval(open('cee-all-articles.txt','r', encoding='utf-8').read())

myc = {}

goodarts = []

for entry in fileeopen:
	article,params = entry
	
	countries = []
	
	for param in params:
		name,value = param
		if name=='dalībnieks' and value=='Edgars2007':
			goodarts.append(entry)
		
#
for entry in goodarts:
	article,params = entry
	
	countries = []
	
	for param in params:
		name,value = param

		if name.startswith('valsts'):
			if value in myc:
				myc[value].append(article)
			else:
				myc[value] = [article]
#

fileefsdfdfsdopen = open(r'../public_html/frkraksti.txt','w', encoding='utf-8')
fileefsdfdfsdopen.write(str(myc))