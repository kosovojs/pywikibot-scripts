import urllib.parse
import requests
import json

def main(url):

	url2= requests.get(url)#.read()
	#pywikibot.output(url2.text)

	data = json.loads(url2.text)
	json_data = data

	#json_data = json.loads(file)

	#pywikibot.output(data)
	itemlist = json_data['*'][0]['a']['*']
	#pywikibot.output(itemlist)
	print('Found %s items on PetScan ' % len(itemlist))

	parselist = []
	for item in itemlist:
		enwikiarticle = item['title']
		#pywikibot.output(enwikiarticle)
		parselist.append(enwikiarticle)
		
	return parselist
	
if __name__ == "__main__":
    main()