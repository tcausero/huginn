import pandas as pd

import client.nyt_api as nyt


def test__timestamp_to_string():
    ts = pd.Timestamp('20200225')
    assert nyt._timestamp_to_string(ts) == '20200225'


def test_get_api_key():
    api_key = nyt.get_api_key()
    print(api_key)
    assert type(api_key) == str


def test_get_links():
    date = pd.Timestamp('20200225')
    keyword = 'Point72'

    one_link_list = nyt.get_links(keyword, date, num_links=1)
    link = one_link_list[0]

    five_link_list = nyt.get_links(keyword, date, num_links=5)

    assert type(one_link_list) == list

    assert len(one_link_list) == 1

    assert len(five_link_list) == 5

    assert 'www.nytimes.com' in link
