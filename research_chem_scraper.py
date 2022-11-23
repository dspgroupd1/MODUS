from bs4 import BeautifulSoup 
import requests
import os

class Research_chem_Scraper():
	def get_urls(self):
		r = requests.get('https://research-chemicals-kopen.com/kopen/')
		soup = BeautifulSoup(r.content, 'html.parser')
		urls = []
		for link in soup.find_all('a', href=True):
			if 'https://research-chemicals-kopen.com/kopen/' in link['href']:
				urls.append(str(link['href']))
		#print(urls)
		return urls
	
	def get_names(self):
		drugs = []
		
		urls = self.get_urls()

		for u in urls:
			r = requests.get(u)
			soup = BeautifulSoup(r.content, 'html.parser')

			divs = soup.findAll('h4', 'entry-title')
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
		drug = drug.split()[0]
		if 'SURVIVOR' in drug:		# to exclude=SURVIVOR (= anti-hangover pil)
			return False
		if 'FLUX' in drug:			# to exclude FLUX (= 4-FMA) 
			return False
		if 'NICOTINE' in drug:		# to exclude nicotine
			return False
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

scraper = Research_chem_Scraper()
scraper.get_names()