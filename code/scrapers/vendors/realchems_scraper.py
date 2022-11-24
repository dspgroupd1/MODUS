from bs4 import BeautifulSoup 
import requests
import os

class Realchems_Scraper():
	
	def get_names(self):
		drugs = []

		r = requests.get('https://realchems.nl/head-shop')
		soup = BeautifulSoup(r.content, 'html.parser')

		divs = soup.findAll('a')
		for div in divs:
			drug = div.text.strip()
			drug = self.clean_name(drug)
			if drug:
				#print(drug)
				drugs.append(drug)
		drugs = list(dict.fromkeys(drugs))
		drugs = sorted(drugs)
		# for index, drug in enumerate(sorted(drugs)):
		# 	print(index, drug)
		return drugs

	def clean_name(self, drug):
		if len(drug) > 0:
			drug = drug.split()[0]

		if 'CRYPTO' in drug:	# to exlude crypto tabs
			return False

		if 'Lab' in drug:		# to exlude Lab equipment
			return False
		
		if 'Galaxy' in drug:	# to exlude galaxy tab
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

scraper = Realchems_Scraper()
scraper.get_names()