import os.path
import os, json, re
from bs4 import BeautifulSoup
from collections import defaultdict

to_save = []

for foldername, subfolders, filenames in os.walk('./results'):
	for filename in filenames:
		if not filename.startswith('2024-P8286-'): continue

		file_path = os.path.join(foldername, filename)

		data = json.loads(open(file_path, 'r', encoding='utf-8').read())

		for entry in data:
			if not entry[3].startswith('https://org.olympedia.www./athletes/'): continue

			to_save.append(entry)



with open('./P8286data-2024-janv.json', 'w', encoding='utf-8') as file_w:
	file_w.write(json.dumps(to_save))
