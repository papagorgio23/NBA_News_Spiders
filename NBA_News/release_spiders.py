# This is a program for running the NBA news_articles spider
# Run from the NBA_News directory with this command:
# python release_spiders.py

import scrapy  # object-oriented framework for crawling and scraping
import os  # operating system commands

# make directory for storing complete html code for web page
page_dirname = 'nba_articles'
if not os.path.exists(page_dirname):
	os.makedirs(page_dirname)

# function for walking and printing directory structure
def list_all(current_directory):
    for root, dirs, files in os.walk(current_directory):
        level = root.replace(current_directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

# examine the directory structure
current_directory = os.getcwd()
list_all(current_directory)

# list the avaliable spiders
print('\nScrapy spider names:\n')
os.system('scrapy list')

# for JSON lines we use this command
os.system('scrapy crawl articles_spider -o items.jl')
print('\nJSON lines written to items.jl\n')