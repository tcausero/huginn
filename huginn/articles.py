##################################
# FUNCTIONS TO GET ARTICLE URLs, TEXTS, TITLES

import requests
import os
from pathlib import Path

import pandas as pd
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
    api_key = os.environ.get('NYT_API_KEY')

    if api_key is None:
        raise DotEnvError('No \'NYT_API_KEY\' system environment variable defined')

    return api_key

def get_nyt_url(keyword, date):
    """Construct NYT API URL

    :argument keyword: entity you are interested in
    :argument date: pandas timestemp

    :returns: corresponding url as a string
    """
    begin_date = _timestamp_to_string(date - pd.DateOffset(days=2))
    end_date = _timestamp_to_string(date + pd.DateOffset(months = 1) + pd.DateOffset(days=2))
    start_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    api_key = get_api_key()
    sections = _get_sections()

    url = (start_url+"q={}&fq=section_name:({})&api-key={}&begin_date={}&end_date={}") \
        .format(keyword, sections, api_key, begin_date, end_date)
    return url

def get_article_urls(keyword, date, num_links='all'):
    """ Returns the links to NYT in the month preceding the input date with a keyword input

    Note - we search the month before the anomaly date as well

    :argument keyword: str keyword to search by
    :argument date: pd.Timestamp containing the date of anomaly, to search the month before
    :argument num_links: The number of links to return. Default is all.

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
        if num_links == 'all':
            return articles
        else:
            return articles[:num_links]

def get_article_title_text_images(article_url):
    """Get the images, title and text of ONE article from its url

    :argument article_url: str corresponding to the web url of the article

    :returns the images, title and content of the article as a string
    """
    r = requests.get(article_url)
    soup = BeautifulSoup(r.content, features="lxml")
    try:
        image_links = []
        for link in soup.find_all('img'):
            imgSrc = link.get('src')
            image_links.append(imgSrc)

        article_html_content = soup.find('html').find('body').find('article')

        title = article_html_content.find('header').find('h1').get_text()
        section = article_html_content.find('section')
        div = article_html_content.find('div', {"class": "entry-content"})

        if section: #NYT article
            paragraphs = section.find_all('p')
        else: #NYT blog article
            paragraphs = div.find_all('p')

        text = ' '.join([title+'.'] + [p.get_text() for p in paragraphs])
        return image_links, title, text
    except:
        return None, None, None

def get_articles_title_text_images(keyword, date, num_links = 'all'):
    """Get the images, title and text for ALL articles related to keyword at a specific date

    :argument keyword: str keyword (entity)
    :argument date: pandas datetime (anomaly date)
    :argument num_links: number of links (articles) to consider, default to all

    :returns a dictionary (keys are urls, images, titles and texts), values are a list of str, corresponding to the urls, images, title or text of each article and an int (S), the number of articles that could have been scrapped
    """
    articles_url = get_article_urls(keyword, date, num_links=num_links)
    results = {}
    results['urls'], results['titles'], results['texts'], results['images'] = articles_url, [], [], []
    S = 0
    for url in articles_url:
        images, title, text = get_article_title_text_images(url)
        if images is not None:
            S+=1
            results['titles'].append(title)
            results['texts'].append(text)
            results['images'].append(images)
    return S, results

def get_articles_title_text_images_all_dates(keyword, dates, num_links = 'all'):
    """Get ALL articles urls, images, title and text for ALL dates (anomalies) related to keyword (entity or person)

    :argument keyword: str keyword (entity or person)
    :argument dates: DatetimeIndex of pandas datetime (dtype=datetime64[ns])
    :argument num_links: number of links (articles) to consider, default to all

    :returns a dictionary (keys are titles and texts) of dictionary whose keys are dates (anomalies) and values are lists containing urls, titles, images or text of articles
    """
    results = {'urls': {}, 'titles':{}, 'texts':{}, 'images':{}}
    for i,date in enumerate(dates):
        S, tmp = get_articles_title_text_images(keyword, date, num_links)
        results['urls'][date] = tmp['urls']
        results['titles'][date] = tmp['titles']
        results['texts'][date] = tmp['texts']
        results['images'][date] = tmp['images']
        N=len(tmp['urls'])
        print('anomaly n°{0}: {1} articles were found and {2}% were retrieved'.format(
            str(i+1), str(N), str(int(S/N*100))))
    return results