"""Scrape URLs found in body of Lynx posts for metadata."""
from typing import Optional, List
import requests
import extruct
from bs4 import BeautifulSoup
from clients.log import LOGGER
from api.posts.lynx.utils import http_headers
from w3lib.html import get_base_url


@LOGGER.catch
def scrape_link(url: str) -> Optional[List[dict]]:
    """Replace anchor tags with embedded previews from scraped data."""
    req = requests.get(url, headers=http_headers)
    if req.status_code != 200:
        LOGGER.error(f'Lynx URL {url} threw status code {req.status_code}')
        return None
    elif req.headers.get('content-type', None) and 'text/html' not in req.headers['content-type']:
        LOGGER.error(f'Lynx URL {url} ignored with type {req.headers.get("content-type")}')
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


def render_json_ltd(html: bytes, base_url: str) -> Optional[dict]:
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


def get_title(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch title via extruct with BeautifulSoup fallback."""
    title = None
    if bool(json_ld) and json_ld.get('headline'):
        if isinstance(json_ld.get('headline'), list):
            title = json_ld['headline'][0]
        elif isinstance(json_ld.get('headline'), str):
            title = json_ld.get('headline')
        if bool(title) and isinstance(title, str):
            return title.replace("'", "")
    if bool(json_ld) and json_ld.get('title'):
        if isinstance(json_ld.get('title'), list):
            title = json_ld['title'][0]
        elif isinstance(json_ld.get('title'), str):
            title = json_ld.get('title')
        if bool(title) and isinstance(title, str):
            return title
    # Fallback to BeautifulSoup if target lacks structured data
    elif html.find("title"):
        title = html.find('title').string
    elif html.find("meta", property="og:title"):
        title = html.find("meta", property="og:title").get('content')
    elif html.find("meta", property="twitter:title"):
        title = html.find("meta", property="twitter:title").get('content')
    elif html.find("h1"):
        title = html.find("h1").string
    if title:
        return title.replace("'", "")


def get_image(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch share image via extruct with BeautifulSoup fallback."""
    image = None
    if bool(json_ld) and json_ld.get('image'):
        if isinstance(json_ld['image'], list):
            image = json_ld['image'][0]
            if bool(image) and isinstance(image, dict):
                image = image.get('url')
            if bool(image) and isinstance(image, str):
                return image
        elif isinstance(json_ld.get('image'), dict):
            image = json_ld['image'].get('url')
        if bool(image) and isinstance(image, str):
            return image
    # Fallback to BeautifulSoup if target lacks structured data
    if html.find("meta", property="image"):
        image = html.find("meta", property="image").get('content')
    elif html.find("meta", property="og:image"):
        image = html.find("meta", property="og:image").get('content')
    elif html.find("meta", property="twitter:image"):
        image = html.find("meta", property="twitter:image").get('content')
    return image


def get_description(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch description via extruct with BeautifulSoup fallback."""
    description = None
    if bool(json_ld) and json_ld.get('description'):
        return json_ld['description'].replace("'", "")
    # Fallback to BeautifulSoup if target lacks structured data
    if html.find("meta", property="description"):
        description = html.find("meta", property="description").get('content')
    elif html.find("meta", property="og:description"):
        description = html.find("meta", property="og:description").get('content')
    elif html.find("meta", property="twitter:description"):
        description = html.find("meta", property="twitter:description").get('content')
    if description:
        return description.replace("'", "")


def get_author(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch author name via extruct with BeautifulSoup fallback."""
    author = None
    if bool(json_ld) and json_ld.get('author'):
        if isinstance(json_ld['author'], list):
            author = json_ld['author'][0]
        if bool(author) and isinstance(json_ld['author'], dict):
            author = json_ld['author'].get('name')
        if bool(author) and isinstance(author, str):
            return author
    # Fallback to BeautifulSoup if target lacks structured data
    elif html.find("meta", property="author"):
        author = html.find("meta", property="author").get('content')
    elif html.find("meta", property="twitter:creator"):
        author = html.find("meta", property="twitter:creator").get('content')
    elif html.find("a", attrs={"class": "commit-author"}):
        author = html.find("a", attrs={"class": "commit-author"}).get('href')
    if author:
        return author
    else:
        return ""


def get_publisher(json_ld: dict) -> Optional[str]:
    """Fetch publisher name via extruct with BeautifulSoup fallback."""
    publisher = None
    if bool(json_ld) and json_ld.get('publisher'):
        if isinstance(json_ld['publisher'], list):
            publisher = json_ld['publisher'][0]
        if bool(publisher) and isinstance(json_ld['publisher'], dict):
            publisher = json_ld['publisher'].get('name')
        if bool(publisher) and isinstance(publisher, str):
            return publisher
        return ""


def get_favicon(html: BeautifulSoup, base_url: str) -> Optional[str]:
    """Fetch favicon with BeautifulSoup."""
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


def get_canonical(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch canonical URL via extruct with BeautifulSoup fallback."""
    canonical = None
    if bool(json_ld) and json_ld.get('mainEntityOfPage'):
        if isinstance(json_ld['mainEntityOfPage'], dict):
            canonical = json_ld['mainEntityOfPage'].get('@id')
        elif isinstance(json_ld['mainEntityOfPage'], str):
            return json_ld['mainEntityOfPage']
    # Fallback to BeautifulSoup if target lacks structured data
    if html.find("link", attrs={"rel": "canonical"}):
        canonical = html.find("link", attrs={"rel": "canonical"}).get('href')
    elif html.find("link", attrs={"rel": "og:url"}):
        canonical = html.find("link", attrs={"rel": "og:url"}).get('content')
    elif html.find("link", attrs={"rel": "twitter:url"}):
        canonical = html.find("link", attrs={"rel": "twitter:url"}).get('content')
    return canonical
