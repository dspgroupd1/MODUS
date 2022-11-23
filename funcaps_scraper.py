from bs4 import BeautifulSoup 
import requests
import os
import csv

class FuncapsScraper():
	def __init__(self):
		self.url = 'https://funcaps.nl/research-chemicals.html'

	def get_names(self):
		page = 1
		total_pages = False
		drugs = []
		while True:
			url = self.url + '?p=' + str(page)
			r = requests.get(url)
			soup = BeautifulSoup(r.content, 'html.parser')
			if not total_pages:
				div = soup.find('div', 'field cs-pagination__page-provider')
				total_pages = int(div.text.split('/')[1].strip())
			divs = soup.findAll('div', 'cs-product-tile__name')
			for div in divs:
				drug = div.text.strip()
				drug = self.clean_name(drug)
				if drug:
					drugs.append(drug)
			page += 1
			if page > total_pages:
				break
		drugs = list(dict.fromkeys(drugs))
		drugs = sorted(drugs)
		# for index, drug in enumerate(sorted(drugs)):
		# 	print(index, drug)
		return drugs
		
	def clean_name(self, drug):
		drug = drug.split()[0]

		if 'Muscle' in drug:	# to exlude anaboles
			return False
		if 'MX' in drug:		# to include MXiPr and MXPr
			return drug
			
		if '-' in drug:
			return drug
		if drug.isupper():
			return drug
		if drug[-3:] == 'pam':
			return drug
		if drug[-3:] == 'lam':
			return drug
		if drug[-3:] == 'ine':
			return drug
		return False
	
scraper = FuncapsScraper()
scraper.get_names()