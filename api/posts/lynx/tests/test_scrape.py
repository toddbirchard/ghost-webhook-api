"""Parsing individual URLs and verify JSON-LD is returned."""
import pytest
import requests
import simplejson as json
from bs4 import BeautifulSoup
from mock import Mock

from ..scrape import get_image, render_json_ltd


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
    with open("api/posts/lynx/tests/data/jsonld/post_images_1.json") as file:
        metadata = json.load(file)
        return metadata


@pytest.fixture
def mock_jsonld_2():
    with open("api/posts/lynx/tests/data/jsonld/post_images_2.json") as file:
        metadata = json.load(file)
        return metadata


@pytest.fixture
def mock_jsonld_3():
    with open("api/posts/lynx/tests/data/jsonld/post_images_3.json") as file:
        metadata = json.load(file)
        return metadata


@pytest.fixture
def mock_html_1():
    with open("api/posts/lynx/tests/data/html/post_html_1.html") as file:
        html = BeautifulSoup(file, "html.parser")
        return html


@pytest.fixture
def mock_html_2():
    with open("api/posts/lynx/tests/data/html/post_html_2.html") as file:
        html = BeautifulSoup(file, "html.parser")
        return html


@pytest.fixture
def mock_html_3():
    with open("api/posts/lynx/tests/data/html/post_html_3.html") as file:
        html = BeautifulSoup(file, "html.parser")
        return html


@pytest.fixture
def hackers_fetched_post(headers):
    """Test post payload."""
    site = Mock()
    site.url = "https://hackersandslackers.com/creating-django-views/"
    req = requests.get(site.url, headers=headers)
    site.html = req.text
    with open("api/posts/lynx/tests/data/django_post_json_ld.json") as file:
        site.json_ld = json.load(file)
    return site


def test_render_json_ltd(hackers_fetched_post):
    """Verify JSON-LD content."""
    test_json_ld = render_json_ltd(hackers_fetched_post.url, hackers_fetched_post.html)
    assert test_json_ld == hackers_fetched_post.json_ld


def test_get_image_1(mock_jsonld_1, mock_html_1):
    image = get_image(mock_jsonld_1, mock_html_1)
    assert image == "https://miro.medium.com/max/1200/1*_rYEpi3Crp_pX0lWBbFeOg.jpeg"


def test_get_image_2(mock_jsonld_2, mock_html_2):
    image = get_image(mock_jsonld_2, mock_html_2)
    assert (
        image
        == "https://cdn.vox-cdn.com/thumbor/C65cXI5Wcs45ZiRqvPMNWWVWi2E=/0x65:1920x1070/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/19312831/Evergarden_Screenshot_1.png"
    )


def test_get_image_3(mock_jsonld_3, mock_html_3):
    image = get_image(mock_jsonld_3, mock_html_3)
    assert (
        image
        == "https://imgix.bustle.com/uploads/image/2020/2/21/20b7ba9d-8d72-4278-ad7f-38a1e07e7370-gettyimages-1137737073-removebg-preview.png?w=1200&h=630&q=70&fit=crop&crop=faces&fm=jpg"
    )
