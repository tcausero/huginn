import os
import requests

import pandas as pd
from dotenv import load_dotenv, find_dotenv

from client.exceptions import NytApiError, DotEnvError, ConfigNotFoundError


def _timestamp_to_string(timestamp):
    """Extracts the date from a pandas timestamp and convert to a string

    :returns string of the format: '20190908' (for September 8th, 2019)

    """
    date_dashes = str(timestamp.date()) \
        .replace('-', '')
    return date_dashes


def _get_sections():
    """ Get the desired sections to search from a config file"""

    try:
        with open("client/config/sections.txt", 'r') as f:
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


def get_links(keyword, date, num_links=1):
    """ Returns the links to NYT in the month preceding the input date with a keyword input

    Note - we search before the month before the anomoly date

    :argument keyword: str keyword to search by
    :argument date: pd.Timestamp containing the date of anomaly, to search the month before
    :argument num_links: The number of links to return. Default is one.

    :returns a list of links of length num_links
    """

    api_key = get_api_key()
    sections = _get_sections()

    end_date = _timestamp_to_string(date)
    begin_date = _timestamp_to_string(date - pd.DateOffset(months=2))

    url_request = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&fq=section_name:({})&api-key={}&begin_date={}&end_date={}' \
        .format(keyword, sections, api_key, begin_date, end_date)
    r = requests.get(url_request)
    json_data = r.json()

    # Look for a fault in the returned data
    try:
        fault = json_data['fault']['faultstring']
        raise NytApiError(fault)

    except KeyError:
        links = [x['web_url'] for x in json_data['response']['docs']]
        return links[:num_links]

