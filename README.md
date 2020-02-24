# Newscatcher
Programmatically collect normalized news from (almost) any website.
By [newscatcherapi.com](https://www.newscatcherapi.com).

## Demo
![](gifs/newscatcherdemo.gif)

## Motivation
While working on newscatcherapi -- JSON API to query the news articles,
I came up with an idea to make a simple Python package that would allow
to easily grab the live news data. 

When I used to be a junior data scientist working on my own side projects,
it was difficult for me to operate with external data sources. I knew Python
quite well, but in most cases it was not enough to build proper data pipelines
that required gathering data on my own. 

Even though I do not recommend to use this package for any production systems, I believe that it should be enough to test your assumptions and build some MVPs.

## Installation
`pip install newscatcher`

## Tech/framework used
The package itself is nothing more than a SQLite database with 
RSS feed endpoints for each website and some basic wrapper of
[feedparser][3].

## Code Example/Documentation
Let's review all possible usage of the package. 

In its core, it has a class called *Newscatcher*. This class is all you need in order to get latest news.

After installing your package, import the class:

`from newscatcher import Newscatcher`
 
Now you just need to put a url of a desired news source as an input into our class. 
**Please take the base form url of a website** (without `www.`,neither `https://`, nor `/` at the end of url).

For example: “nytimes”.com, “news.ycombinator.com” or “theverge.com”.

`news_source = Newscatcher('blackfaldslife.com')`

If you have done it right and the source that you chose is presented in our database, you will get a variable with 3 components and 1 method:

- `news_source.website` -- the same string that you entered inside the class.
- `news_source.news` -- a list of a feedparser dictionary with latest news presented on the website. 
- `news_source.headlines` -- a list with latest headlines presented on the website.
- `news_source.print_headlines()` -- print headlines of all latest articles.

Each element of *news* list is a json object with all relevant and available information regarding an article. If you want to know more about the attributes that you can extract from this json, go check the official documentation of feedparser following this link: [feedparser\_attributes][4]. You can find everything that begins with *entries[i]*. But be aware that not all the attributes are provided by the news website. 

If for some reason you do not like classes, you can always import 2 main methods and use them separately.

`from newscatcher import get_news`
`news = get_news('wired.co.uk')`

or

`from newscatcher import get_headlines`
`news = get_headlines('wired.co.uk')`


## Licence
MIT


[3]:	%3Chttps://pythonhosted.org/feedparser/index.html%3E
[4]:	%3Chttps://pythonhosted.org/feedparser/reference.html%3E
