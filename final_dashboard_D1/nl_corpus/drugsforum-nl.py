import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time
from classes import *
import pandas as pd

class DrugsForumNLThread(Thread):
	# get thread content here; everything else should be done through drugsforumscraper
	def get_thread_content(self):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.content, 'html.parser')
		self.content = soup.find('article', class_='message-body js-selectToQuote').text.replace('\n',' ')

# main drugsforum.nl scraper
class DrugsForumNLScraper():
	def __init__(self):
		self.url = 'https://drugsforum.nl'
		self.dir_path = '.'

	# write list of Thread objects in a csv file
	def write_threads(self, threads, page, category):
		dir_path = self.dir_path
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)
		df = pd.DataFrame.from_records([t.to_dict() for t in threads])
		
		if page == 1:
			df.to_csv(category + 'drugsforumnl_threads.csv', index=False, sep=',')
		else:
			df.to_csv(category + 'drugsforumnl_threads.csv', mode='a', index=False, header=False, sep=',')

	def get_all_category_threads(self):
		for i in range(1,48):
			self.get_threads('research_chemicals',i)
		for i in range(107,117):
			self.get_threads('drugs_general',i)
		for i in range(1,114):
			self.get_threads('trip_reports',i)

	# get threads and their details and call write function
	def get_threads(self, category, page=1):
		print("page: ", page)
		if category == 'research_chemicals':
			url = 'https://drugsforum.nl/forums/research-chemicals.37/page-'+str(page)+'?order=post_date&direction=desc'
		if category == 'drugs_general':
			url = 'https://drugsforum.nl/forums/drugs.10/page-'+str(page)+'?order=post_date&direction=desc'
		if category == 'trip_reports':
			url = 'https://drugsforum.nl/forums/trip-reports.21/page-'+str(page)+'?order=post_date&direction=desc'
		print(url)
		threads = []
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')
		divs = soup.findAll('div', class_='structItem-cell structItem-cell--main')
		detail_divs = soup.findAll('div', class_='structItem-cell structItem-cell--meta')
		for div, detail_div in zip(divs, detail_divs):
			sticky_i = div.find('i', class_='structItem-status structItem-status--sticky')
			if sticky_i:
				continue
				
			title_div = div.find('div', class_='structItem-title')
			if not title_div:
				print("TITLE DIV ERROR")
				continue
			thread_url = self.url + title_div.find('a')['href']
			try:
				thread_id = int(thread_url.split('.')[-1].replace('/',''))
			except:
				print("ID ERROR")
				continue

			thread_title = title_div.text.strip()

			thread_date = div.find('li', class_='structItem-startDate').find('time')['datetime'][0:10]

			thread_comments = detail_div.findAll('dd')[0].text
			if 'K' in thread_comments:
				thread_comments = int(thread_comments.split('K')[0])*1000
			
			thread_views = detail_div.findAll('dd')[1].text
			if 'K' in thread_views:
				thread_views = int(thread_views.split('K')[0])*1000

			threads.append(DrugsForumNLThread(
				url = thread_url,
				title = thread_title,
				date = thread_date,
				views = thread_views,
				comments = thread_comments,
				thread_id = thread_id,
				forum = 'drugsforum-nl'
			))


		for i,thread in enumerate(threads):
			thread.get_thread_content()
			print(i,thread.thread_id, thread.title)
		self.write_threads(threads, page, category)

scraper = DrugsForumNLScraper()
scraper.get_all_category_threads()