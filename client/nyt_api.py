import requests
import json

import pandas as pd


def _timestamp_to_string(timestamp):
    """Extracts the date from a pandas timestamp and convert to a string

    :returns string of the format: '20190908' (for September 8th, 2019)

    """
    date_dashes = str(timestamp.date()) \
        .replace('-', '')
    return date_dashes


def get_links(api_key, keyword, date, num_links=1):
    """ Returns the links to NYT in the month preceding the input date with a keyword input

    Note - we search before the month before the anomoly date

    :argument keyword: str keyword to search by
    :argument date: pd.Timestamp containing the date of anomaly, to search the month before
    :argument num_links: The number of links to return. Default is one.

    :returns a list of links of length num_links
    """

    api_key = 'jLIh1Z3tdtM8XfULe3EHGrv55fAodXCk'

    end_date = _timestamp_to_string(date)
    begin_date = _timestamp_to_string(date - pd.DateOffset(months=2))

    url_request = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&api-key={}&begin_date={}&end_date={}' \
        .format(keyword, api_key, begin_date, end_date)
    r = requests.get(url_request)
    json_data = r.json()
    links = [x['web_url'] for x in json_data['response']['docs']]

    return links[:num_links]