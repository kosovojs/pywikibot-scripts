
from pywikiapi import wikipedia
from helpers import clean_api
import os, pymysql, json, re, requests
# Connect to English Wikipedia

class Petscan:
	site = None

	def __init__(self):
		self.site = wikipedia('www', 'wikidata')

	def get_data(self, json= None, qs = None, id = None, return_type = 'raw'):
		if json:
			res = requests.get('https://petscan.wmflabs.org/?', params=json)
		if qs:
			res = requests.get('https://petscan.wmflabs.org/?{}'.format(qs))

		resp = res.json()

		if return_type == 'raw':
			return resp['*'][0]['a']['*']

		if return_type == 'wd':
			return [d['q'] for d in resp['*'][0]['a']['*']]
