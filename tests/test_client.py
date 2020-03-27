import pytest

import client.client_obj


@pytest.fixture
def client_point72():

    return 5

def test_get_nyt_links(client_point72):
    five = client_point72
    assert five == 5