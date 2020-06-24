"""Test parsing individual URLs."""
import simplejson as json
import pytest
import requests
from mock import Mock
from api.posts.lynx.scrape import render_json_ltd


@pytest.fixture
def link_json():
    """Test post payload."""
    link = Mock()
    link.url = 'https://hackersandslackers.com/'
    with open('api/posts/lynx/tests/data/home_json_ld.json') as file:
        link.data = json.load(file)
    return link


@pytest.fixture
def link_url():
    """Test post payload."""
    link = Mock()
    link.url = 'https://hackersandslackers.com/'
    return link


@pytest.fixture
def link_html(link_url):
    """Test raw HTML of target."""
    html = Mock()
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(link_url.url, headers=headers)
    html.text = req.text
    return html


def test_render_json_ltd(link_url, link_html, link_json):
    """Verify JSON-LD content."""
    test_json_ld = render_json_ltd(link_url.url, link_html.text)
    assert test_json_ld == link_json.data
