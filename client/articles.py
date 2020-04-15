##################################
# FUNCTIONS TO GET ARTICLE URLs, TEXTS, TITLES

import requests
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup

from .exceptions import NytApiError, DotEnvError, ConfigNotFoundError

def _timestamp_to_string(timestamp):
    """Extracts the date from a pandas timestamp and convert to a string

    :returns string of the format: '20190908' (for September 8th, 2019)

    """
    date_dashes = str(timestamp.date()).replace('-', '')
    return date_dashes

def _get_sections():
    """ Get the desired sections to search from a config file"""
    file_path = Path(os.path.dirname(os.path.abspath(__file__))) / 'config' / 'sections.txt'
    print(file_path)

    try:
        with open(file_path, 'r') as f:
            sections = f.readlines()

    except FileNotFoundError:
        raise ConfigNotFoundError('Config file not found')

    section_list = ["\"{}\"".format(line.strip()) for line in sections]
    section_string = " ".join(section_list)

    return section_string

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
    """Construct NYT API URL

    :argument keyword: entity you are interested in
    :argument date: pandas timestemp

    :return: corresponding url as a string
    """
    begin_date = _timestamp_to_string(date - pd.DateOffset(months=1))
    end_date = _timestamp_to_string(date + pd.DateOffset(months=1))
    start_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    api_key = get_api_key()
    sections = _get_sections()

    url = (start_url+"q={}&fq=section_name:({})&api-key={}&begin_date={}&end_date={}") \
        .format(keyword, sections, api_key, begin_date, end_date)
    return url

def get_article_urls(keyword, date, num_links=1):
    """ Returns the links to NYT in the month preceding the input date with a keyword input

    Note - we search the month before the anomaly date as well

    :argument keyword: str keyword to search by
    :argument date: pd.Timestamp containing the date of anomaly, to search the month before
    :argument num_links: The number of links to return. Default is one.

    :returns a list of links of length num_links (corresponding to articles for ONE anomaly)
    """

    url = get_nyt_url(keyword, date)
    r = requests.get(url)

    # Look for a fault in the returned data
    try:
        fault = r.json()['fault']['faultstring']
        raise NytApiError(fault)

    except KeyError:
        #only keep article (not multimedia content)
        articles = [news['web_url'] for news in r.json()['response']['docs'] if news['document_type'] == 'article']
        return articles[:num_links]

<<<<<<< HEAD
def get_article_title_text(article_url):
    """Get the title and text of ONE article from its url
    
    :argument article_url: str corresponding to the web url of the article
    
    :returns the title and content of the article as a string (or the empty string is the article was not found)
=======
def get_article_text(article_url):
    """Get the text of ONE article from its url

    :argument article_url: str corresponding to the web url of the article

    :returns the content of the article as a string (or the empty string is the artile was not found)
>>>>>>> 61ba8fb1bba9fcaa1c4bd215162dc3bfbc57fbf0
    """
    r = requests.get(article_url)
    soup = BeautifulSoup(r.content, features="lxml")
    try:
        article_html_content = soup.find('html').find('body').find('article')
        title = article_html_content.find('header').find('h1').get_text()
        paragraphs = article_html_content.find('section', attrs = {'name':'articleBody'}).find_all('p')
        text = ' '.join([title+'.'] + [p.get_text() for p in paragraphs])
        return title, text
    except:
        print('Problem with the following url:', article_url)
        return '', ''

<<<<<<< HEAD
def get_articles_title_text(keyword, date, num_links = 1):
    """Get the title and text for ALL articles related to keyword at a specific date
    
    :argument keyword: str keyword (entity)
    :argument date: pandas datetime (anomaly date)
    :argument num_links: number of links (articles) to consider
    
    :returns a dictionary (keys are titles and texts), values are a list of str, corresponding to the title or text of each article
=======
def get_articles_text(keyword, date, num_links = 1):
    """Get the text for ALL articles related to keyword at a specific date

    :argument keyword: str keyword (entity)
    :argument date: pandas datetime (anomaly date)
    :argument num_links: number of links (articles) to consider

    :returns a list of str, corresponding to the text of each article
>>>>>>> 61ba8fb1bba9fcaa1c4bd215162dc3bfbc57fbf0
    """
    articles_url = get_article_urls(keyword, date, num_links=num_links)
    results = {}
    results['titles'], results['texts'] = [], []
    for url in articles_url:
        title, text = get_article_title_text(url) 
        results['titles'].append(title)
        results['texts'].append(text)
    return results

<<<<<<< HEAD
def get_articles_title_text_all_dates(keyword, dates, num_links = 1):
    """Get ALL articles title and text for ALL dates (anomalies) related to keyword (entity or person)
    
    :argument keyword: str keyword (entity or person)
    :argument dates: DatetimeIndex of pandas datetime (dtype=datetime64[ns])
    :argument num_links: number of links (articles) to consider
    
    :returns a dictionary (keys are titles and texts) of dictionary whose keys are dates (anomalies) and values are lists containing title or text of articles
    """
    results = {'titles':{}, 'texts':{}}
    for date in dates:
        temp = get_articles_title_text(keyword, date, num_links)
        titles = temp['titles']
        texts = temp['texts']
        results['titles'][date] = titles
        results['texts'][date] = texts
    return results
=======
def get_article_title(article_url):
    """Get the title of ONE article from its url

    :argument article_url: str corresponding to the web url of the article

    :returns the title of the article as a string (or the empty string is the artile was not found)
    """
    r = requests.get(article_url)
    soup = BeautifulSoup(r.content, features="lxml")
    try:
        article_html_content = soup.find('html').find('body').find('article')
        title = article_html_content.find('header').find('h1').get_text()
        return title
    except:
        print('Problem with the following url:', article_url)
        return ''

def get_article_images(article_url):
    """Get the url to each image for ONE article from its url

    :argument article_url: str corresponding to the web url of the article

    :returns a list of links to all images in the article
    """
    r  = requests.get(article_url) #Download website source
    data = r.text  #Get the website source as text
    soup = BeautifulSoup(data) #Setup a "soup" which BeautifulSoup can search
    image_links = []
    for link in soup.find_all('img'):  #Cycle through all 'img' tags
        imgSrc = link.get('src')   #Extract the 'src' from those tags
        image_links.append(imgSrc)    #Append the source to 'links'
    return image_links  #Print 'links'

def get_articles_title(keyword, date, num_links = 1):
    """Get the title for ALL articles related to keyword at a specific date

    :argument keyword: str keyword (entity)
    :argument date: pandas datetime (anomaly date)
    :argument num_links: number of links (articles) to consider

    :returns a list of str, corresponding to the title of each article
    """
    articles_url = get_article_urls(keyword, date, num_links=num_links)
    return [get_article_title(article_url) for article_url in articles_url]

def get_articles_images(keyword, date, num_links=1):
    """Get the images for ALL articles related to keyword at a specific date

    :argument keyword: str keyword (entity)
    :argument date: pandas datetime (anomaly date)
    :argument num_links: number of links (articles) to consider

    :returns a list of lists, each nested list corresponding to all images in the respective article
    """
    articles_url = get_article_urls(keyword, date, num_links=num_links)
    return [get_article_images(article_url) for article_url in articles_url]

def get_articles_text_all_dates(keyword, dates, num_links = 1):
    """Get ALL articles text for ALL dates (anomalies) related to keyword (entity or person)

    :argument keyword: str keyword (entity or person)
    :argument dates: DatetimeIndex of pandas datetime (dtype=datetime64[ns])
    :argument num_links: number of links (articles) to consider

    :returns a dictionary whose keys are dates (anomalies) and values are lists containing text of articles
    """
    return {date: get_articles_text(keyword, date, num_links) for date in dates}

def get_articles_title_all_dates(keyword, dates, num_links = 1):
    """Get ALL articles title for ALL dates (anomalies) related to keyword (entity or person)

    :argument keyword: str keyword (entity or person)
    :argument dates: DatetimeIndex of pandas datetime (dtype=datetime64[ns])
    :argument num_links: number of links (articles) to consider

    :returns a dictionary whose keys are dates (anomalies) and values are lists containing title of articles
    """
    return {date: get_articles_title(keyword, date, num_links) for date in dates}

def get_articles_images_all_dates(keyword, dates, num_links=1):
    """Get ALL article images for ALL dates (anomalies) related to keyword (entity or person)

    :argument keyword: str keyword (entity or person)
    :argument dates: DatetimeIndex of pandas datetime (dtype=datetime64[ns])
    :argument num_links: number of links (articles) to consider

    :returns a dictionary whose keys are dates (anomalies) and values are list of lists containing links to images in the article
    """
    return {date: get_articles_images(keyword, date, num_links) for date in dates}
>>>>>>> 61ba8fb1bba9fcaa1c4bd215162dc3bfbc57fbf0
