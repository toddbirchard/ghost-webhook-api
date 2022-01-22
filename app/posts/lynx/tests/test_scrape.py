"""Parsing individual URLs and verify JSON-LD is returned."""
import json

import pytest
import requests
from bs4 import BeautifulSoup
from mock import Mock

from ..scrape import scrape_metadata_from_url


@pytest.fixture
def headers() -> dict:
    """Spoofed browser headers."""
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }


@pytest.fixture
def mock_jsonld_1():
    """First example of parsed JSON-LD metadata."""
    with open(
        "app/posts/lynx/tests/data/jsonld/post_images_1.json", encoding="utf-8"
    ) as file:
        metadata = json.load(file)
        return metadata


@pytest.fixture
def mock_jsonld_2():
    """Second example of parsed JSON-LD metadata."""
    with open(
        "app/posts/lynx/tests/data/jsonld/post_images_2.json", encoding="utf-8"
    ) as file:
        metadata = json.load(file)
        return metadata


@pytest.fixture
def mock_jsonld_3():
    """Third example of parsed JSON-LD metadata."""
    with open(
        "app/posts/lynx/tests/data/jsonld/post_images_3.json", encoding="utf-8"
    ) as file:
        metadata = json.load(file)
        return metadata


@pytest.fixture
def mock_html_1():
    """First example parsed HTML file."""
    with open(
        "app/posts/lynx/tests/data/html/post_html_1.html", encoding="utf-8"
    ) as file:
        html = BeautifulSoup(file, "html.parser")
        return html


@pytest.fixture
def mock_html_2():
    """Second example parsed HTML file."""
    with open(
        "app/posts/lynx/tests/data/html/post_html_2.html", encoding="utf-8"
    ) as file:
        html = BeautifulSoup(file, "html.parser")
        return html


@pytest.fixture
def mock_html_3():
    """Third example parsed HTML file."""
    with open(
        "app/posts/lynx/tests/data/html/post_html_3.html", encoding="utf-8"
    ) as file:
        html = BeautifulSoup(file, "html.parser")
        return html


@pytest.fixture
def hackers_fetched_post(headers):
    """Test post payload."""
    site = Mock()
    site.url = "https://hackersandslackers.com/creating-django-views/"
    req = requests.get(site.url, headers=headers)
    site.html = req.text
    with open(
        "app/posts/lynx/tests/data/django_post_json_ld.json", encoding="utf-8"
    ) as file:
        site.json_ld = json.load(file)
    return site


def test_scrape_metadata_from_url():
    """Verify JSON-LD content."""
    bookmark_card = scrape_metadata_from_url("https://hackersandslackers.com")
    assert bookmark_card[0] == "bookmark"
    assert bookmark_card[1]["url"] == "https://hackersandslackers.com"
    assert bookmark_card[1]["metadata"]["title"] == "Hackers and Slackers"
    assert (
        bookmark_card[1]["metadata"]["image"]
        == "https://hackersandslackers.com/images/share.png"
    )
    assert (
        bookmark_card[1]["metadata"]["icon"]
        == "https://hackersandslackers.com/images/logo-small@2x.png"
    )
