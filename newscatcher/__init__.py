__version__ = '0.2.0'

# Retrieve and analyze
# 24/7 streams of news data
import sqlite3
#import requests
import feedparser
import pkg_resources
from tldextract import extract

DB_FILE = pkg_resources.resource_filename('newscatcher', 'data/package_rss.db')


class Query:
    # Query class used to build subsequent sql queries
    def __init__(self):
        self.params = {'website': None, 'topic': None}

    def build_conditional(self, field, sql_field):
        # single conditional build
        field = field.lower()
        sql_field = sql_field.lower()

        if self.params[field] != None:
            conditional = "{} = '{}'".format(sql_field, self.params[field])
            return conditional
        return

    def build_where(self):
        # returning the conditional from paramters
        # the post "WHERE"
        conditionals = []

        conv = {'topic': 'topic_unified', 'website': 'clean_url'}

        for field in conv.keys():
            cond = self.build_conditional(field, conv[field])
            if cond != None:
                conditionals.append(cond)

        if conditionals == []:
            return

        conditionals[0] = 'WHERE ' + conditionals[0]
        conditionals = ''' AND '.join([x for x in conditionals if x != None])
		+ ' ORDER BY IFNULL(Globalrank,999999);'''

        return conditionals

    def build_sql(self):
        # build sql on user qeury
        db = sqlite3.connect(DB_FILE, isolation_level=None)
        sql = 'SELECT rss_url from rss_main ' + self.build_where()

        db.close()
        return sql


def clean_url(dirty_url):
    # website.com
    dirty_url = dirty_url.lower()
    o = extract(dirty_url)
    return o.domain + '.' + o.suffix


class Newscatcher:
    # search engine
    def build_sql(self):
        if self.topic is None:
            sql = '''SELECT rss_url from rss_main 
					 WHERE clean_url = '{}';'''
            sql = sql.format(self.url)
            return sql

    def __init__(self, website, topic=None):
        # init with given params
        website = website.lower()
        self.url = clean_url(website)
        self.topic = topic

    def get_headlines(self, n=None):
        if self.topic is None:
            sql = '''SELECT rss_url,topic_unified, language, clean_country from rss_main 
					 WHERE clean_url = '{}' AND main = 1;'''
            sql = sql.format(self.url)
        else:
            sql = '''SELECT rss_url, topic_unified, language, clean_country from rss_main 
					 WHERE clean_url = '{}' AND topic_unified = '{}';'''
            sql = sql.format(self.url, self.topic)

        db = sqlite3.connect(DB_FILE, isolation_level=None)

        try:
            rss_endpoint, topic, language, country = db.execute(sql).fetchone()
            feed = feedparser.parse(rss_endpoint)
        except:
            if self.topic is not None:
                sql = '''SELECT rss_url from rss_main 
					 WHERE clean_url = '{}';'''
                sql = sql.format(self.url)

                if len(db.execute(sql).fetchall()) > 0:
                    db.close()
                    print('Topic is not supported')
                    return
                else:
                    print('Website is not supported')
                    return
                    db.close()
            else:
                print('Website is not supported')
                return

        if feed['entries'] == []:
            db.close()
            print('\nNo headlines found check internet connection or query parameters\n')
            return

        title_list = []
        for article in feed['entries']:
            if 'title' in article:
                title_list.append(article['title'])
            if n != None:
                if len(title_list) == n:
                    break

        return title_list

    def print_headlines(self, n=None):
        headlines = self.get_headlines(n)

        i = 1
        for headline in headlines:
            if i < 10:
                print(str(i) + '.   |  ' + headline)
                i += 1
            elif i in list(range(10, 100)):
                print(str(i) + '.  |  ' + headline)
                i += 1
            else:
                print(str(i) + '. |  ' + headline)
                i += 1

    def get_news(self, n=None):
        # return results based on current stream
        if self.topic is None:
            sql = '''SELECT rss_url,topic_unified, language, clean_country from rss_main 
					 WHERE clean_url = '{}' AND main = 1;'''
            sql = sql.format(self.url)
        else:
            sql = '''SELECT rss_url, topic_unified, language, clean_country from rss_main 
					 WHERE clean_url = '{}' AND topic_unified = '{}';'''
            sql = sql.format(self.url, self.topic)

        db = sqlite3.connect(DB_FILE, isolation_level=None)

        try:
            rss_endpoint, topic, language, country = db.execute(sql).fetchone()
            feed = feedparser.parse(rss_endpoint)
        except:
            if self.topic is not None:
                sql = '''SELECT rss_url from rss_main 
					 WHERE clean_url = '{}';'''
                sql = sql.format(self.url)

                if len(db.execute(sql).fetchall()) > 0:
                    db.close()
                    print('Topic is not supported')
                    return
                else:
                    print('Website is not supported')
                    return
                    db.close()
            else:
                print('Website is not supported')
                return

        if feed['entries'] == []:
            db.close()
            print('\nNo results found check internet connection or query parameters\n')
            return

        if n == None or len(feed['entries']) <= n:
            articles = feed['entries']  # ['summary']#[0].keys()
        else:
            articles = feed['entries'][:n]

        db.close()
        return {'url': self.url, 'topic': topic,
                'language': language, 'country': country, 'articles': articles}


def describe_url(website):
    # return newscatcher fields that correspond to the url
    website = website.lower()
    website = clean_url(website)
    db = sqlite3.connect(DB_FILE, isolation_level=None)

    sql = "SELECT clean_url, language, clean_country, topic_unified from rss_main WHERE clean_url = '{}' and main == 1 ".format(
        website)
    results = db.execute(sql).fetchone()
    main = results[-1]

    if main == None:
        print('\nWebsite not supported\n')
        return

    if len(main) == 0:
        print('\nWebsite note supported\n')
        return

    sql = "SELECT DISTINCT topic_unified from rss_main WHERE clean_url == '{}'".format(website)
    topics = db.execute(sql).fetchall()
    topics = [x[0] for x in topics]

    ret = {'url': results[0], 'language': results[1], 'country': results[2], 'main_topic': main, 'topics': topics}

    return ret


def urls(topic=None, language=None, country=None):
    # return urls that matches users parameters
    if language != None:
        language = language.lower()

    if country != None:
        country = country.upper()

    if topic != None:
        topic = topic.lower()

    db = sqlite3.connect(DB_FILE, isolation_level=None)
    quick_q = Query()
    inp = {'topic': topic, 'language': language, 'country': country}
    for x in inp.keys():
        quick_q.params[x] = inp[x]

    conditionals = []
    conv = {'topic': 'topic_unified', 'website': 'clean_url',
            'country': 'clean_country', 'language': 'language'}

    for field in conv.keys():
        try:
            cond = quick_q.build_conditional(field, conv[field])
        except:
            cond = None

        if cond != None:
            conditionals.append(cond)

    sql = ''

    if conditionals == []:
        sql = 'SELECT clean_url from rss_main '
    else:
        conditionals[0] = ' WHERE ' + conditionals[0]
        conditionals = ' AND '.join([x for x in conditionals if x is not None])
        conditionals += ' AND main = 1 ORDER BY IFNULL(Globalrank,999999);'
        sql = 'SELECT DISTINCT clean_url from rss_main' + conditionals

    ret = db.execute(sql).fetchall()
    if len(ret) == 0:
        print('\nNo websites found for given parameters\n')
        return

    db.close()
    return [x[0] for x in ret]