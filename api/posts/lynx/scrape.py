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
    json_ld = render_json_ltd(url, req.content)
    parsed_metadata = metadata_parser.MetadataParser(
        url=url,
        url_headers=http_headers,
        search_head_only=False
    )
    card = ["bookmark", {
                "type": "bookmark",
                "url": get_canonical(parsed_metadata),
                "metadata": {
                    "url": get_canonical(parsed_metadata),
                    "title": get_title(parsed_metadata, json_ld),
                    "description": get_description(parsed_metadata, json_ld),
                    "author": get_author(parsed_metadata, html, json_ld),
                    "publisher": get_publisher(json_ld),
                    "thumbnail": get_image(parsed_metadata, json_ld),
                    "icon": get_favicon(parsed_metadata, html, json_ld, get_domain(url))
                    }
                }
            ]
    return card


def render_json_ltd(url: str, html) -> Optional[dict]:
    """Fetch JSON-LD structured data."""
    metadata = extruct.extract(
        html,
        base_url=get_domain(url),
        syntaxes=['json-ld'],
        uniform=True
    )['json-ld']
    if bool(metadata) and isinstance(metadata, list):
        metadata = metadata[0]
    return metadata


def get_title(parsed_metadata, _data: dict) -> Optional[str]:
    """Scrape parsed_metadata title."""
    title = None
    if bool(_data) and _data.get('title'):
        title = _data['title']
    elif bool(_data) and _data.get('headline'):
        title = _data['headline']
    elif parsed_metadata.get_metadata('title'):
        title = parsed_metadata.get_metadata('title')
    elif parsed_metadata.get_metadata('og:title'):
        title = parsed_metadata.get_metadata('og:title')
    elif parsed_metadata.get_metadata('twitter:title'):
        title = parsed_metadata.get_metadata('twitter:title')
    if title:
        title = title[0].split('|')[0]
    return title


def get_image(parsed_metadata, _data: dict) -> Optional[str]:
    """Scrape parsed_metadata `share image`."""
    image = None
    if bool(_data):
        if isinstance(_data, list):
            image = _data[0]
        if image is not None and isinstance(_data, dict):
            image = image.get('image')
        if isinstance(_data, str):
            return image
    if parsed_metadata.get_metadata('og:image'):
        image = parsed_metadata.get_metadata('og:image')
    elif parsed_metadata.get_metadata('twitter:image'):
        image = parsed_metadata.get_metadata('twitter:image')
    return image


def get_description(parsed_metadata, _data: dict) -> Optional[str]:
    """Scrape parsed_metadata description."""
    description = None
    if bool(_data) and _data.get('description'):
        description = _data['description']
    elif parsed_metadata.get_metadata('description'):
        description = parsed_metadata.get_metadata('description')
    elif parsed_metadata.get_metadata('og:description'):
        description = parsed_metadata.get_metadata('og:description')
    elif parsed_metadata.get_metadata('twitter:description'):
        description = parsed_metadata.get_metadata('twitter:description')
    return description


def get_author(parsed_metadata, html, _data: dict) -> Optional[str]:
    """Scrape author name."""
    author = None
    if bool(_data) and _data.get('author'):
        if type(_data['author']) == list:
            _author = _data['author'][0]
            author = _author.get('name')
        elif type(_data['author']) == dict:
            author = _data['author'].get('name')
    elif parsed_metadata.get_metadata('author'):
        author = parsed_metadata.get_metadata('author')
    elif parsed_metadata.get_metadata('article:author'):
        author = parsed_metadata.get_metadata('article:author')
    elif parsed_metadata.get_metadata('twitter:creator'):
        author = parsed_metadata.get_metadata('twitter:creator')
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


def get_favicon(parsed_metadata, html, _data: dict, base_url: str) -> Optional[str]:
    """Scrape favicon image."""
    favicon = None
    if bool(_data) and _data.get('logo'):
        favicon = _data['logo'].get('url')
    if parsed_metadata.get_metadata('shortcut icon'):
        favicon = parsed_metadata.get_metadata('shortcut icon')
    elif parsed_metadata.get_metadata('icon'):
        favicon = parsed_metadata.get_metadata('icon')
    elif parsed_metadata.get_metadata('shortcut'):
        favicon = parsed_metadata.get_metadata('shortcut')
    elif parsed_metadata.get_metadata('apple-touch-icon'):
        favicon = parsed_metadata.get_metadata('apple-touch-icon')
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


def get_canonical(parsed_metadata) -> Optional[str]:
    """Get parsed_metadata canonical URL."""
    canonical = None
    if parsed_metadata.get_metadata('canonical'):
        canonical = parsed_metadata.get_metadata('canonical')[0]
    return canonical
