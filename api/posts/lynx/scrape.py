"""Scrape URLs found in body of Lynx posts for metadata."""
from typing import Optional, List
import requests
import metadata_parser
import extruct
from bs4 import BeautifulSoup
from api.log import LOGGER
from api.posts.lynx.utils import http_headers


@LOGGER.catch
def scrape_link(url) -> Optional[List[dict]]:
    """Scrape links embedded in post for metadata to build preview cards."""
    req = requests.get(url, headers=http_headers)
    if req.status_code != 200:
        LOGGER.error(f'Invalid Lynx URL threw {req.status_code}: {url}')
        return None
    html = BeautifulSoup(req.content, 'html.parser')
    json_ld = render_json_ltd(url, req.text)
    page = metadata_parser.MetadataParser(
        url=url,
        url_headers=http_headers,
        search_head_only=False
    )
    card = ["bookmark", {
                "type": "bookmark",
                "url": get_canonical(page),
                "metadata": {
                    "url": get_canonical(page),
                    "title": get_title(page, json_ld),
                    "description": get_description(page, json_ld),
                    "author": get_author(page, html, json_ld),
                    "publisher": get_publisher(json_ld),
                    "thumbnail": get_image(page, json_ld),
                    "icon": get_favicon(page, html, json_ld, get_domain(url))
                    }
                }
            ]
    return card


def render_json_ltd(url, html) -> Optional[dict]:
    """Fetch JSON-LD structured data."""
    metadata = extruct.extract(
        html,
        base_url=get_domain(url),
        syntaxes=['json-ld'],
        uniform=True
    )['json-ld']
    try:
        metadata = metadata[0]
    except IndexError:
        metadata = metadata
    return metadata


def get_title(page, _data: dict) -> Optional[str]:
    """Scrape page title."""
    title = None
    if bool(_data) and _data.get('title'):
        title = _data['title']
    elif bool(_data) and _data.get('headline'):
        title = _data['headline']
    elif page.get_metadatas('title'):
        title = page.get_metadatas('title')
    elif page.get_metadatas('og:title'):
        title = page.get_metadatas('og:title')
    elif page.get_metadatas('twitter:title'):
        title = page.get_metadatas('twitter:title')
    if title:
        title = title[0].split('|')[0]
    return title


def get_image(page, _data: dict) -> Optional[str]:
    """Scrape page `share image`."""
    image = None
    if bool(_data) and _data.get('image'):
        image = _data['image'].get('image')
    elif page.get_metadatas('og:image'):
        image = page.get_metadatas('og:image')[0]
    elif page.get_metadatas('twitter:image'):
        image = page.get_metadatas('twitter:image')[0]
    return image


def get_description(page, _data: dict) -> Optional[str]:
    """Scrape page description."""
    description = None
    if bool(_data) and _data.get('description'):
        description = _data['description']
    elif page.get_metadatas('description'):
        description = page.get_metadatas('description')[0]
    elif page.get_metadatas('og:description'):
        description = page.get_metadatas('og:description')[0]
    elif page.get_metadatas('twitter:description'):
        description = page.get_metadatas('twitter:description')[0]
    return description


def get_author(page, html, _data: dict) -> Optional[str]:
    """Scrape author name."""
    author = None
    if bool(_data) and _data.get('author'):
        if type(_data['author']) == list:
            _author = _data['author'][0]
            author = _author.get('name')
        elif type(_data['author']) == dict:
            author = _data['author'].get('name')
    elif page.get_metadatas('author'):
        author = page.get_metadatas('author')[0]
    elif page.get_metadatas('article:author'):
        author = page.get_metadatas('article:author')[0]
    elif page.get_metadatas('twitter:creator'):
        author = page.get_metadatas('twitter:creator')[0]
    elif html.find("a", attrs={"class": "commit-author"}):
        author = html.find("a", attrs={"class": "commit-author"}).get('href')
    return author


def get_publisher(_data: dict) -> Optional[str]:
    """Scrape publisher name."""
    publisher = None
    if bool(_data) and _data.get('publisher'):
        if type(_data['publisher']) == list:
            _publisher = _data['publisher'][0]
            publisher = _publisher.get('name')
        elif type(_data['publisher']) == dict:
            publisher = _data['publisher'].get('name')
    return publisher


def get_favicon(page, html, _data: dict, base_url: str) -> Optional[str]:
    """Scrape favicon image."""
    favicon = None
    if bool(_data) and _data.get('logo'):
        favicon = _data['logo'].get('url')
    if page.get_metadatas('shortcut icon'):
        favicon = page.get_metadatas('shortcut icon')[0]
    elif page.get_metadatas('icon'):
        favicon = page.get_metadatas('icon')[0]
    elif page.get_metadatas('shortcut'):
        favicon = page.get_metadatas('shortcut')[0]
    elif page.get_metadatas('apple-touch-icon'):
        favicon = page.get_metadatas('apple-touch-icon')[0]
    elif html.find("link", attrs={"rel": "fluid-icon"}):
        favicon = html.find("link", attrs={"rel": "fluid-icon"}).get('href')
    elif html.find("link", attrs={"rel": "mask-icon"}):
        favicon = html.find("link", attrs={"rel": "mask-icon"}).get('href')
    elif html.find("link", attrs={"rel": "icon"}):
        favicon = html.find("link", attrs={"rel": "icon"}).get('href')
    elif html.find("link", attrs={"rel": "shortcut icon"}):
        favicon = html.find("link", attrs={"rel": "shortcut icon"}).get('href')
    if favicon and favicon[0] != 'http':
        favicon = base_url + favicon
    if favicon is None:
        favicon = base_url + '/favicon.ico'
    return favicon


def get_domain(url: str) -> Optional[str]:
    """Get site root domain name."""
    domain = url.split('://')[1]
    name = domain.split('/')[0]
    return f'https://{name}'


def get_canonical(page) -> Optional[str]:
    """Get page canonical URL."""
    canonical = None
    if page.get_metadatas('canonical'):
        canonical = page.get_metadatas('canonical')[0]
    return canonical
