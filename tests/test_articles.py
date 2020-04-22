import pandas as pd

from huginn import articles


def test__timestamp_to_string():
    ts = pd.Timestamp('20200225')
    assert articles._timestamp_to_string(ts) == '20200225'


def test_get_api_key():
    api_key = articles.get_api_key()
    assert type(api_key) == str


def test__get_sections():
    sections = articles._get_sections()

    assert type(sections) == str
    assert "&" not in sections


def test_get_links():
    date = pd.Timestamp('20180212')
    keyword = 'Point72'

    one_link_list = articles.get_article_urls(keyword, date, num_links=1)
    link = one_link_list[0]

    five_link_list = articles.get_article_urls(keyword, date, num_links=5)

    assert type(one_link_list) == list

    assert len(one_link_list) == 1

    assert len(five_link_list) == 5

    assert 'www.nytimes.com' in link
