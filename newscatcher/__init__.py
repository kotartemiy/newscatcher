__version__ = '0.1.0'

import sqlite3
import requests
import feedparser
from urllib.parse import urlsplit
import pkg_resources

DB_FILE = pkg_resources.resource_filename('newscatcher', 'data/newscatcher_package_v2.db')

class Newscatcher:
    
    def __init__(self, website = 'news.ycombinator.com'):
        self.website = website
        self.news = get_news(website)
        self.headlines = get_headlines(website)
        
    def print_headlines(self, n = None):
        if n == None:
            i = 1
            for headline in self.headlines:
                if i < 10:
                    print(str(i) + '.   |  ' + headline )
                    i += 1
                elif i in list(range(10,100)):
                    print(str(i) + '.  |  ' + headline )
                    i += 1                
                else:
                    print(str(i) + '. |  ' + headline )
                    i += 1       
    
        else:
            i = 1
            for headline in self.headlines:
                if i < 10 and i <= n:
                    print(str(i) + '.   |  ' + headline )
                    i += 1
                elif i in list(range(10,100)) and i <= n:
                    print(str(i) + '.  |  ' + headline )
                    i += 1                
                elif i >= 100 and i <= n:
                    print(str(i) + '. |  ' + headline )
                    i += 1  
        
        

def get_news(website = 'news.ycombinator.com'):
    if type(website) != str:
        raise TypeError("input must be a string") 
    
    db = sqlite3.connect(DB_FILE, isolation_level=None)
    try:
        rss_endpont = db.execute('''select rss_endpoint from rss_table where url = \'''' +\
                                 website +'''\';''').fetchone()[0]
    except TypeError:
        raise Exception('website is not supported')
    feed = feedparser.parse(rss_endpont)
    if feed['entries'] == []:
        raise Exception('check internet connection / website is not supported')
        
    return feed['entries']


def get_headlines(website = 'news.ycombinator.com'):
    feed_entries = get_news(website)
    title_list = []
    for article in feed_entries:
        if 'title' in article:
            title_list.append(article['title'])
    return title_list
