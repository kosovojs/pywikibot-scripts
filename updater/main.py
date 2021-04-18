from wikidata import Wikidata
#from wiki_api import WikiAPI

wd = Wikidata()
#api = WikiAPI()

def main():
	allWDData = wd.getMainData()
	goodItems = wd.goodItems
	allWDData = wd.langLists

	#resFromWDAPI = api.getWikidataItems(goodItems)
	
	#for lang in allWDData:
	#	currLangData = allWDData[lang]


if __name__ == '__main__':
	main()