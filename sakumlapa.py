#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pywikibot import page
import requests
from datetime import date, datetime, timedelta
import pywikibot
import json
from collections import Counter
import operator
import urllib.parse

botflag = False

headers = {
	'User-Agent': 'w:lv:Veidne:Skatītākie raksti Vikipēdijā'.encode('utf8')
}

lvwiki_namespaces = tuple(['Portāls:', 'Portāls:', 'Attēls:', 'File:', 'Veidnes diskusija:', 'Template talk:', 'Modulis:', 'Module:', 'Gadget:', 'Gadget:', 'MediaWiki:', 'MediaWiki:', 'Media:', 'Media:', 'Portāla diskusija:', 'Portāla diskusija:', 'Gadget talk:', 'Gadget talk:', 'Education Program talk:', 'Education Program talk:', 'Attēla diskusija:', 'File talk:', 'Palīdzība:', 'Help:', 'Education Program:', 'Education Program:', 'MediaWiki diskusija:', 'MediaWiki talk:', 'Gadget definition:', 'Gadget definition:', 'Special:', 'Special:', 'Vikipēdija:', 'Project:', 'Vikiprojekta diskusija:', 'Vikiprojekta diskusija:', 'Vikiprojekts:', 'Vikiprojekts:', 'Moduļa diskusija:', 'Module talk:', 'Veidne:', 'Template:', 'Dalībnieks:', 'User:', 'Diskusija:', 'Talk:', 'Kategorija:', 'Category:', 'Kategorijas diskusija:', 'Category talk:', 'Dalībnieka diskusija:', 'User talk:', 'Tēma:', 'Topic:', 'Gadget definition talk:', 'Gadget definition talk:', 'Vikipēdijas diskusija:', 'Project talk:', 'Palīdzības diskusija:', 'Help talk:', 'Dalībniece:', 'Lietotājs:', 'Dalībnieces diskusija:', 'Lietotāja diskusija:', 'VP:', 'WP:', 'Wikipedia:', 'Image:', 'Image talk:'])

site = pywikibot.Site("lv", "wikipedia")

def get_viewcount(pageview_data):
	if 'items' not in pageview_data:
		return 0

	return sum([day['views'] for day in pageview_data['items']])

def make_view_link(article):
	return "https://pageviews.toolforge.org/?project=lv.wikipedia.org&platform=desktop&agent=user&redirects=0&range=latest-20&pages={}".format(urllib.parse.quote(article))

def merge_pageview_date(data):
	summary_data = {}
	for day_data in data:
		dict1 = {article1['article']: article1['views'] for article1 in day_data['items'][0]['articles']}
		summary_data = dict(Counter(dict1)+Counter(summary_data))

	sorted_data = sorted(summary_data.items(), key=operator.itemgetter(1), reverse=True)

	return sorted_data


class MostViewedPages:
	configuration = {}
	final_list = []
	filtered_list = []
	desktop_viewcounts = {}
	date_objects = []

	def __init__(self):
		self.load_configuration()

	def load_configuration(self):
		configuration = pywikibot.Page(site,'Dalībnieks:Edgars2007/Skatītākie raksti/configuration.json')
		configuration = configuration.get()
		configuration = json.loads(configuration)
		self.configuration = configuration

	def get_data(self):
		files = []
		first_date = datetime.now()

		day_count = int(self.configuration['config']['daycount'])

		for daySUB in range(day_count):
			date_object = (first_date - timedelta(days=1) - timedelta(days=daySUB)).date()
			self.date_objects.append(date_object)
			date_string = date_object.strftime("%Y/%m/%d")
			urltoopen = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/lv.wikipedia.org/all-access/{}'.format(date_string)
			res = requests.get(urltoopen, headers=headers).json()
			if 'title' in res and res['title'] == 'Not found.':
				continue
			files.append(res)

		return files

	def filter_articles(self, data):
		titles_to_exclude = self.configuration['config']['exclude']

		filtered_list = []

		for entry in data:
			title, _ = entry
			if title in titles_to_exclude:
				continue

			if title.replace('_',' ').startswith(lvwiki_namespaces):
				continue

			filtered_list.append(entry)

		self.filtered_list = filtered_list

	def check_article_validity(self, article):
		print(article)
		ordered_dates = self.date_objects
		first_date = ordered_dates[-1].strftime("%Y%m%d")
		last_date = ordered_dates[0].strftime("%Y%m%d")

		platform = 'desktop'

		url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/lv.wikipedia.org/{}/user/{}/daily/{}/{}".format(platform, article, first_date, last_date)
		res = requests.get(url, headers=headers).json()

		viewcount_desktop = get_viewcount(res)
		viewcount_desktop = 1 if viewcount_desktop == 0 else viewcount_desktop

		platform = 'all-access'

		url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/lv.wikipedia.org/{}/user/{}/daily/{}/{}".format(platform, article, first_date, last_date)
		res = requests.get(url, headers=headers).json()

		viewcount_all = get_viewcount(res)
		viewcount_all = 1 if viewcount_all == 0 else viewcount_all

		desktop_percentage = round(viewcount_desktop / viewcount_all, 4)
		self.desktop_viewcounts.update({article: desktop_percentage})

		return True

	def populate_final_list(self):
		article_count_to_include = self.configuration['config']['articlecount']
		final_list = []
		curr_count = 0
		for entry in self.filtered_list:
			if curr_count == article_count_to_include:
				break
			article, _ = entry

			is_valid = True
			# is_valid = self.check_article_validity(article)
			if is_valid:
				final_list.append(entry)
				curr_count += 1

		self.final_list = final_list

		for idx in range(0,25):
			self.check_article_validity(self.filtered_list[idx][0])

	def save_template(self):
		pagetosave = pywikibot.Page(site,'Veidne:Skatītākie raksti Vikipēdijā/Sagatave')

		articles = "]]|\n[[".join([f[0].replace('_',' ') for f in self.final_list])

		description = "{{hlist|Pagājušajā nedēļā skatītākais:<br />[[" + articles + "]]}}<noinclude>\n{{dokumentācija}}</noinclude>"

		pagetosave.text = description
		pagetosave.save(summary='bots: atjaunināts', botflag=botflag, minor=False)

	def save_statistics(self):
		table_header = '{|class="sortable wikitable"\n|-\n! Lapa !! Skatījumi !! Desktop skatījumi\n'

		output_parts = []

		cnt = 0

		article_count_to_include = self.configuration['config']['articlecount']

		for entry in self.filtered_list[:100]:
			cnt += 1
			desktop_views = self.desktop_viewcounts[entry[0]] if entry[0] in self.desktop_viewcounts else ""
			border = ""

			if cnt == article_count_to_include+1:
				border = 'style="border-top: 5px solid gray;"'

			curr_part = "|- {}\n| [[{}]] || [{} {}] || {}".format(border, entry[0].replace('_',' '), make_view_link(entry[0]), entry[1], desktop_views)
			output_parts.append(curr_part)

		table = table_header + '\n'.join(output_parts) + "\n|}"

		addeddates = [f.strftime("%d.%m") for f in self.date_objects[::-1]]

		outputtext = 'Iekļautie datumi: '+', '.join(addeddates)+'.\n\n'+table

		report_pageE = pywikibot.Page(site,'Veidne:Skatītākie raksti Vikipēdijā/Statistika')
		report_pageE.text = outputtext
		report_pageE.save(summary='bots: atjaunināts', botflag=botflag, minor=False)

	def handle(self):
		page_view_data = self.get_data()
		sorted_pageviews = merge_pageview_date(page_view_data)
		self.filter_articles(sorted_pageviews)
		self.populate_final_list()

		self.save_template()
		self.save_statistics()

inst = MostViewedPages()
inst.handle()
