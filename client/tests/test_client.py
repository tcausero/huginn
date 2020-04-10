import time

import pytest
import pandas as pd

from ..client import Client

@pytest.fixture
def client_point72():
    key_word = "Point72"

    cl = Client(key_word)
    cl.get_anomalies()

    return cl


def test_get_text(client_point72):
    time.sleep(45)
    client_point72.get_text()

    text = client_point72.text

    assert type(text) == dict

    assert len(text) <= 10

    for ts, text in text.items():
        assert type(ts) == pd.Timestamp
        assert type(text) == list


