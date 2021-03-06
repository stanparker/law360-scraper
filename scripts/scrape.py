import urllib2
import csv
import json
import random
import time

import sys

from datetime import datetime
from collections import defaultdict

from bs4 import BeautifulSoup as bs


class Scraper(object):

	current_date = time.strftime('%m/%d/%y')

	current_date = datetime.strptime(current_date, '%m/%d/%y')

	DISTRICTS = {
		"01": "District 1",
		"02": "District 2",
		"03": "District 3",
		"04": "District 4",
		"05": "District 5",
		"06": "District 6",
		"07": "District 7",
		"08": "District 8",
		"09": "District 9",
		"10": "District 10",
		"11": "District 11",
		"12": "District 12",
		"13": "District 13",
		"14": "District 14"
	}


	while True:

		month = int(raw_input('> Enter month (01-12): '))

		day = int(raw_input('> Enter day (01-31): '))

		year = int(raw_input('> Enter year (1900-2016): '))


		input_date = str(month)+'/'+str(day)+'/'+str(year)

		input_date = datetime.strptime(input_date, "%m/%d/%Y")

		if len(str(month)) > 2 or len(str(month)) < 1:

			print 'I need a TWO-digit number for a month: 02 or 10!'

			continue

		elif month > 12:
			print 'There are only 12 months in a year! '

			continue

		elif day > 31:
			
			print 'Anything more than 31 for the day won\'t work!'

			continue

		elif year > 2016:

			print 'I can\'t predict the future! Pick the current or previous year!'

			continue

		elif len(str(day)) > 2 or len(str(day)) < 1:

			print 'I need a TWO-digit number for a day: 01 or 31!'

			continue

		elif len(str(year)) > 4 or len(str(year)) < 4:

			print 'I need a FOUR-digit number for a year: 2015 or 2016!'

			continue


		elif input_date > current_date:

			print 'I can\'t predict the future! Enter a date current or previous date'
			
			continue

		else:
			break


	message = [

		'No more burning the midnight oil!',
		'Giiiddddyyy up!',
		'This is too easy.',
		'I wanted to be a flat screen TV when I grew up, but I became a computer instead.',
		'Is it time to go home yet?',
		'Take a second to enjoy the fact you don\'t have to do this by hand.',
		'Here\'s a joke while you wait: What do you call a camel with three humps? Pregnant!',
		'Beyonce has 24 hours in a day. You do too.',
		'From WBEZ Chicago it\'s Cereal. One bowl eaten week by week.',
		'You just jumped over jumpman.',
		'If walked on the runway in high heels in front of the whole town I\'d fall down. And my momma\'d cry, when she realized, I ain\'t pageant material.',
		'I fell in love in the back of a cop car. I couldn\'t see your eyes because the damn lights were shining in my eyes.',
		'I tried to make ramen in the coffee pot, and I broke everything.',
		'I typed your symptoms into the thing up here, and it says you could have network connectivity problems.',
		'There\'s only one thing I hate more than lying: skim milk. Which is water that\'s lying about being milk.',
		'I really only listen to, like, German death reggae and Halloween sound effects records from the 1950s.'
	]


	def init(self):

		m = str(self.month)
		d = str(self.day)
		y = str(self.year)

		tables = self.scrape(m,d,y)

		case_numbers = self.get_case_numbers(tables)

		self.create_json(case_numbers)


	def scrape(self, month, day, year):

		url = "http://stanparker.net/law360/texas.php?date=" + month + '/' + day + '/' + year

		print 'Collecting data... ' + random.choice(self.message)

		page = urllib2.urlopen(url)

		soup = bs(page, 'html5lib')

		tables = soup.find_all('tbody')

		return tables


	def get_case_numbers (self, tables):

		cases = []

		print len(tables)

		for i in range(0,len(tables)):
			
			links = tables[i].find_all('a')

			for link in links[::2]:
				text = link.get_text()

				cases.append(text)

		return cases


	def create_json (self, cases):
		
		d = []

		for case in cases:
			id_num = case[:2]

			obj = {}

			try:

				obj['district'] = self.DISTRICTS[id_num]
				obj['cases'] = case

				d.append(obj)

			except KeyError:
				pass


		json.dump(d, open('law_cases.json', 'w'))

		with open('law_cases.json') as file:

			f = json.load(file)

		file.close()

		grouped = defaultdict(list)

		for district in f:
			grouped[district['district'][0]].append(district)

		print 'Done! ' + random.choice(self.message)


if __name__ == '__main__':

	s = Scraper()
	s.init()