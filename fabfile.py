from fabric.api import *

def scrape_data():
	local('python scripts/scrape.py')

def convert_data():
	local('node scripts/convert.js')

@task
def init():
	scrape_data()
	convert_data()
