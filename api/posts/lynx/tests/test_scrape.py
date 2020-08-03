"""Parsing individual URLs and verify JSON-LD is returned."""
import simplejson as json
import pytest
import requests
from mock import Mock
from api.posts.lynx.scrape import render_json_ltd


@pytest.fixture
def headers() -> dict:
    """Spoofed browser headers."""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }


@pytest.fixture
def hackers_fetched_post(headers):
    """Test post payload."""
    site = Mock()
    site.url = 'https://hackersandslackers.com/creating-django-views/'
    req = requests.get(site.url, headers=headers)
    site.html = req.text
    with open('api/posts/lynx/tests/data/django_post_json_ld.json') as file:
        site.json_ld = json.load(file)
    return site


def test_render_json_ltd(hackers_fetched_post):
    """Verify JSON-LD content."""
    test_json_ld = render_json_ltd(
        hackers_fetched_post.url,
        hackers_fetched_post.html
    )
    assert test_json_ld == hackers_fetched_post.json_ld
