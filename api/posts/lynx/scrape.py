"""Scrape URLs found in body of Lynx posts for metadata."""
from typing import Optional, List
import requests
import extruct
from bs4 import BeautifulSoup
from api.log import LOGGER
from api.posts.lynx.utils import http_headers
from w3lib.html import get_base_url


@LOGGER.catch
def scrape_link(url) -> Optional[List[dict]]:
    """Replace anchor tags with embedded previews from scraped data."""
    req = requests.get(url, headers=http_headers)
    if req.status_code != 200:
        LOGGER.error(f'Invalid Lynx URL threw {req.status_code}: {url}')
        return None
    html = BeautifulSoup(req.content, 'html.parser')
    base_url = get_base_url(req.content, url)
    json_ld = render_json_ltd(req.content, base_url)
    card = ["bookmark", {
                "type": "bookmark",
                "url": get_canonical(json_ld, html),
                "metadata": {
                    "url": get_canonical(json_ld, html),
                    "title": get_title(json_ld, html),
                    "description": get_description(json_ld, html),
                    "author": get_author(json_ld, html),
                    "publisher": get_publisher(json_ld),
                    "thumbnail": get_image(json_ld, html),
                    "icon": get_favicon(html, base_url)
                    }
                }
            ]
    return card


def render_json_ltd(html, base_url: str) -> Optional[dict]:
    """Fetch JSON-LD structured data."""
    metadata = extruct.extract(
        html,
        base_url=base_url,
        syntaxes=['json-ld'],
        uniform=True
    )['json-ld']
    if bool(metadata) and isinstance(metadata, list):
        metadata = metadata[0]
    return metadata


def get_title(_data: dict, html) -> Optional[str]:
    """Scrape parsed_metadata title."""
    title = None
    if bool(_data) and _data.get('headline'):
        if isinstance(_data.get('headline'), list):
            title = _data['headline'][0]
        elif isinstance(_data.get('headline'), str):
            title = _data.get('headline')
        if isinstance(title, str):
            return title
    if bool(_data) and _data.get('title'):
        if isinstance(_data.get('title'), list):
            title = _data['title'][0]
        elif isinstance(_data.get('title'), str):
            title = _data.get('title')
        if isinstance(title, str):
            return title
    elif html.title.string:
        title = html.title.string
    elif html.find("meta", property="og:title"):
        title = html.find("meta", property="og:title").get('content')
    elif html.find("meta", property="twitter:title"):
        title = html.find("meta", property="twitter:title").get('content')
    elif html.find("h1"):
        title = html.find("h1").string
    return title


def get_image(_data: dict, html) -> Optional[str]:
    """Scrape parsed_metadata `share image`."""
    image = None
    if bool(_data) and _data.get('image'):
        if isinstance(_data['image'], list):
            image = _data['image'][0]
            if isinstance(image, dict):
                image = image.get('url')
            if isinstance(image, str):
                return image
        elif isinstance(_data.get('image'), dict):
            image = _data['image'].get('url')
        if isinstance(image, str):
            return image
    if html.find("meta", property="image"):
        image = html.find("meta", property="image").get('content')
    elif html.find("meta", property="og:image"):
        image = html.find("meta", property="og:image").get('content')
    elif html.find("meta", property="twitter:image"):
        image = html.find("meta", property="twitter:image").get('content')
    return image


def get_description(_data: dict, html) -> Optional[str]:
    """Scrape parsed_metadata description."""
    description = None
    if bool(_data) and _data.get('description'):
        return _data['description']
    if html.find("meta", property="description"):
        description = html.find("meta", property="description").get('content')
    elif html.find("meta", property="og:description"):
        description = html.find("meta", property="og:description").get('content')
    elif html.find("meta", property="twitter:description"):
        description = html.find("meta", property="twitter:description").get('content')
    return description


def get_author(_data: dict, html) -> Optional[str]:
    """Scrape author name."""
    author = None
    if bool(_data) and _data.get('author'):
        if isinstance(_data['author'], list):
            author = _data['author'][0].get('name')
        elif isinstance(_data['author'], dict):
            author = _data['author'].get('name')
        if isinstance(author, str):
            return author
    elif html.find("meta", property="author"):
        author = html.find("meta", property="author").get('content')
    elif html.find("meta", property="twitter:creator"):
        author = html.find("meta", property="twitter:creator").get('content')
    elif html.find("a", attrs={"class": "commit-author"}):
        author = html.find("a", attrs={"class": "commit-author"}).get('href')
    return author


def get_publisher(_data: dict) -> Optional[str]:
    """Scrape publisher name."""
    publisher = None
    if bool(_data) and _data.get('publisher'):
        if isinstance(_data['publisher'], list):
            publisher = _data['publisher'][0].get('name')
        elif isinstance(_data['publisher'], dict):
            publisher = _data['publisher'].get('name')
    return publisher


def get_favicon(html, base_url: str) -> Optional[str]:
    """Scrape favicon image."""
    favicon = None
    if html.find("link", attrs={"rel": "icon"}):
        favicon = html.find("link", attrs={"rel": "icon"}).get('href')
    elif html.find("link", attrs={"rel": "fluid-icon"}):
        favicon = html.find("link", attrs={"rel": "fluid-icon"}).get('href')
    elif html.find("link", attrs={"rel": "mask-icon"}):
        favicon = html.find("link", attrs={"rel": "mask-icon"}).get('href')
    elif html.find("link", attrs={"rel": "icon"}):
        favicon = html.find("link", attrs={"rel": "icon"}).get('href')
    elif html.find("link", attrs={"rel": "shortcut icon"}):
        favicon = html.find("link", attrs={"rel": "shortcut icon"}).get('href')
    if favicon and 'http' not in favicon:
        favicon = base_url + favicon
    if favicon is None:
        favicon = base_url + '/favicon.ico'
    return favicon


def get_domain(url: str) -> Optional[str]:
    """Get site root domain name."""
    domain = url.split('://')[1]
    name = domain.split('/')[0]
    return f'https://{name}'


def get_canonical(_data: dict, html) -> Optional[str]:
    """Get parsed_metadata canonical URL."""
    canonical = None
    if bool(_data) and _data.get('mainEntityOfPage'):
        if isinstance(_data['mainEntityOfPage'], dict):
            canonical = _data['mainEntityOfPage'].get('@id')
        elif isinstance(_data['mainEntityOfPage'], str):
            return _data['mainEntityOfPage']
    if html.find("link", attrs={"rel": "canonical"}):
        canonical = html.find("link", attrs={"rel": "canonical"}).get('href')
    elif html.find("link", attrs={"rel": "og:url"}):
        canonical = html.find("link", attrs={"rel": "og:url"}).get('content')
    elif html.find("link", attrs={"rel": "twitter:url"}):
        canonical = html.find("link", attrs={"rel": "twitter:url"}).get('content')
    return canonical
