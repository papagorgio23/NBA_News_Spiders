import scrapy
import os.path
from NBA_Scrapy.items import NBANewsItem
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


team_urls = [
    'https://www.nba.com/hawks/news',
    'https://www.nba.com/celtics/news',
    'https://www.nba.com/nets/news',
    'https://www.nba.com/hornets/news',
    'https://www.nba.com/bulls/news',
    'https://www.nba.com/cavaliers/news',
    'https://www.nba.com/mavericks/news',
    'https://www.nba.com/nuggets/news',
    'https://www.nba.com/pistons/news',
    'https://www.nba.com/warriors/news',
    'https://www.nba.com/rockets/news',
    'https://www.nba.com/pacers/news',
    'https://www.nba.com/clippers/news',
    'https://www.nba.com/lakers/news',
    'https://www.nba.com/grizzlies/news',
    'https://www.nba.com/heat/news',
    'https://www.nba.com/bucks/news',
    'https://www.nba.com/timberwolves/news',
    'https://www.nba.com/pelicans/news/',
    'https://www.nba.com/knicks/news',
    'https://www.nba.com/thunder/news',
    'https://www.nba.com/magic/news',
    'https://www.nba.com/sixers/news',
    'https://www.nba.com/suns/news',
    'https://www.nba.com/blazers/news',
    'https://www.nba.com/kings/news',
    'https://www.nba.com/spurs/news',
    'https://www.nba.com/raptors/news',
    'https://www.nba.com/jazz/news',
    'https://www.nba.com/wizards/news'
]

def get_article_urls():
    opts = Options()
    opts.headless = True
    driver = webdriver.Chrome(options=opts)

    # initialize url list
    start_urls = []

    # loop through each team's website with selenium
    for team in team_urls:
        team_name = team.split("/")[-2]
        print("Opening the {} website\n".format(team_name))
        driver.get(team)
        time.sleep(2)

        ## There is an accept cookies button sometimes that is in the way of the load more button
        try:
            print("Trying to click the Stupid Cookies button...\n")
            stupid_button = driver.find_element_by_id("nba_tos_close_button")
            stupid_button.click()
        except Exception:
            print("There was no Cookie button! Moving on...\n")
            pass

        ## Error handling for some websites that are different...
        try:
            ## Load more articles on the webpage
            print("Loading all the articles. This might take a few extra seconds...\n")
            # 12 news articles
            time.sleep(2)
            button = driver.find_element_by_id("load-more")

            # 24 news articles
            button.click()
            time.sleep(2)

            # 36 news articles
            button.click()
            print("...Loading more articles...\n")
            time.sleep(2)

            # 48 news articles
            button.click()
            time.sleep(2)

            # 60 news articles
            button.click()
            print("...Still loading more articles...\n")
            time.sleep(2)

            # 72 news articles
            button.click()
            time.sleep(2)

            # 84 news articles
            button.click()
            print("...Almost there...\n")
            time.sleep(2)

            # 96 news articles
            button.click()
            print("Finished loading 96 news articles about the {}!!\n".format(team_name))
            time.sleep(2)

        except Exception:
            print("You created me headless, aka BLIND!!, I couldn't find where the 'Load More' Button is for the {}.. I'm sorry I failed you. :(\n".format(team_name))
            pass
        
        ## Get all the links on the page
        try:
            # Get links to each article
            links = driver.find_elements_by_css_selector('.post__title a')

            # put them all into a list
            for link in links:
                start_urls.append(link.get_attribute('href'))
            print("You just stole {} articles! Hopefully you don't get busted!\n".format(len(start_urls)))
        except Exception:
            print("I couldn't find any links for the {}.. Maybe they just aren't news worth?\n".format(team_name))
            pass
    
    # quit the browser
    driver.quit()

    # filter out false links with 'node'
    start_urls = [k for k in start_urls if '/node/' not in k]

    # filter out Video links
    start_urls = [k for k in start_urls if '/video/' not in k]

    # filter out Photo Gallery links
    start_urls = [k for k in start_urls if '/gallery/' not in k]


    # Good Work
    print("Some of the links were fakes. But you are smarter than them and figured out a way to get around their nonsense!")
    print("You officially stole {} valid news articles about {} NBA teams!".format(len(start_urls), len(team_urls)))
    print("You deserve a drink!\n")

    # return the list of urls
    return start_urls

        



class ArticlesSpider(scrapy.Spider):
    name = 'articles_spider'
    allowed_domains = ['nba.com']
    start_urls = get_article_urls()

    def parse(self, response):

        # report which url scrapy is currently on
        self.logger.info('Parse function called on {}'.format(response.url))

        # Steal the actual html webpage for our record
        page = response.url.split("/")[-1]
        filename = 'nba_articles/%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)



        # Collect the specific fields from each article
        loader = ItemLoader(item=NBANewsItem(), response=response)
        loader.add_value('team', response.url.split("/")[3])
        loader.add_value('url', response.url)
        loader.add_xpath('date', '//div[@class="author-block__post-date"]/text()')
        loader.add_css('title', '.h1::text')
        loader.add_xpath('tags', '//*[@class="tag__link"]/text()')
        loader.add_css('article', 'p')

        # load all items into scrapy
        item = loader.load_item()

        # I hate how the string outputs are in a list and I couldn't figure out why the ItemLoader made it that way 
        # this code overwrites the ItemLoader for a couple metrics to make they show up in the right order and format
        item['team'] = response.url.split("/")[3]
        item['url'] = response.url

        # Fin (French for Done and Done!)
        yield item

