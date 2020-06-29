"""Test parsing individual URLs."""
import simplejson as json
import pytest
import requests
from mock import Mock
from api.posts.lynx.scrape import render_json_ltd
from .utils import headers


@pytest.fixture
def headers():
    return headers


@pytest.fixture
def hackers_homepage(headers):
    """Test post payload."""
    site = Mock()
    site.url = 'https://hackersandslackers.com/'
    site.html = requests.get(site.url, headers=headers)
    with open('api/posts/lynx/tests/data/home_json_ld.json') as file:
        site.json_ld = json.load(file)
    return site


def test_render_json_ltd(hackers_homepage):
    """Verify JSON-LD content."""
    test_json_ld = render_json_ltd(
        hackers_homepage.url,
        hackers_homepage.html
    )
    assert test_json_ld == hackers_homepage.json_ld
