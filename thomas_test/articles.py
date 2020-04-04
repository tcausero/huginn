import requests
import json
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from exceptions import NytApiError, DotEnvError
from bs4 import BeautifulSoup

def _timestamp_to_string(timestamp):
    """Extracts the date from a pandas timestamp and convert to a string

    :returns string of the format: '20190908' (for September 8th, 2019)

    """
    date_dashes = str(timestamp.date()).replace('-', '')
    return date_dashes

def get_api_key():
    """Uses .env files to fetch and return the NYT API Key"""
    dotenv_path = find_dotenv()

    if not dotenv_path:
        raise DotEnvError('No .env file found')

    load_dotenv(dotenv_path)
    api_key = os.environ.get('NYT_API_KEY')

    if api_key is None:
        raise DotEnvError('No \'NYT_API_KEY\' variable defined in .env')

    return api_key

def get_nyt_url(keyword, date):
    #get NYT URL (API) from keyword and date
    begin_date = _timestamp_to_string(date - pd.DateOffset(months=1))
    end_date = _timestamp_to_string(date)
    start_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    api_key = get_api_key()
    url = (start_url+"q={0}&begin_date={1}&end_date={2}&sort=relevance&api-key="+api_key).format(keyword, begin_date, end_date)
    return url

def get_article_urls(keyword, date, num_links = 1):
    """ Returns the links to NYT in the month preceding the input date with a keyword input
    Return all urls for ONE date

    Note - we search before the month before the anomaly date

    :argument keyword: str keyword to search by
    :argument date: pd.Timestamp containing the date of anomaly, to search the month before
    :argument num_links: The number of links to return. Default is one.

    :returns a list of links of length num_links
    """
    
    url = get_nyt_url(keyword, date)
    r = requests.get(url)
    
    # Look for a fault in the returned data
    try:
        fault = r.json()['fault']['faultstring']
        raise NytApiError(fault)

    except KeyError:
        #only keep article (not multimedia content)
        articles = [news['web_url'] for news in r.json()['response']['docs'] if news['document_type']=='article']
        return articles[:num_links]

def get_article_text(article_url):
    #get text of ONE article
    r = requests.get(article_url)
    soup = BeautifulSoup(r.content, features="lxml")
    try:
        article_html_content = soup.find('html').find('body').find('article')
        title = article_html_content.find('header').find('h1').get_text()
        paragraphs = article_html_content.find('section', attrs = {'name':'articleBody'}).find_all('p')
        return ' '.join([title+'.'] + [p.get_text() for p in paragraphs])
    except:
        print('Problem with the following url:', article_url)
        return ''

def get_articles_text(keyword, date, num_links = 1):
    #get text of a list of articles (for one date)
    articles_url = get_article_urls(keyword, date, num_links = num_links)
    return [get_article_text(article_url) for article_url in articles_url]

def get_article_title(article_url):
    #get title of ONE article
    r = requests.get(article_url)
    soup = BeautifulSoup(r.content, features="lxml")
    try:
        article_html_content = soup.find('html').find('body').find('article')
        title = article_html_content.find('header').find('h1').get_text()
        return title
    except:
        print('Problem with the following url:', article_url)
        return ''

def get_articles_title(keyword, date, num_links = 1):
    #get title of a list of articles (for one date)
    articles_url = get_article_urls(keyword, date, num_links = num_links)
    return [get_article_title(article_url) for article_url in articles_url]

def get_articles_text_all_dates(keyword, dates, num_links = 1):
    #return dictionary with text of articles associated to dates
    return {date: get_articles_text(keyword, date, num_links) for date in dates}

def get_articles_title_all_dates(keyword, dates, num_links = 1):
    #return dictionary with title of articles associated to dates
    return {date: get_articles_title(keyword, date, num_links) for date in dates}