import time

import pytest
import pandas as pd

from ..huginn import Huginn

@pytest.fixture
def point72():
    key_word = "Point72"

    cl = Huginn(key_word)
    cl.get_anomalies()

    return cl


def test_get_text(point72):
    time.sleep(45)
    point72.get_text()

    text = point72.text

    assert type(text) == dict

    assert len(text) <= 10

    for ts, text in text.items():
        assert type(ts) == pd.Timestamp
        assert type(text) == list


