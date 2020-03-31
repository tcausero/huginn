import os

import pytest
import pandas as pd

import client.getting_anomalies as anom
from client.client_obj import client


@pytest.fixture
def client_point72():
    entity = "Point72"

    interest = pd.read_csv(os.path.join('client', 'interest_cache', entity + '.csv'), index_col=0)
    interest.index = interest.index.astype('datetime64[ns]')

    cl = client(entity, interest)
    cl.get_anomalies(method=anom.version_3, lookback=10)

    return cl


def test_get_nyt_links(client_point72):
    client_point72.get_nyt_links(sleeptime=7)

    links = client_point72.links

    assert type(links) == dict

    assert len(client_point72.links) <= 10

    for time, link in links.items():
        assert type(time) == pd.Timestamp
        assert type(link) == list


