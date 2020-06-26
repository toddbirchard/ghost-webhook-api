"""Scrape URLs found in body of Lynx posts for metadata."""
import requests
import metadata_parser
import extruct
from bs4 import BeautifulSoup
from api.log import LOGGER
from .utils import headers


@LOGGER.catch
def scrape_link(link):
    """Scrape links embedded in post for metadata to build preview cards."""
    req = requests.get(link, headers=headers)
    html = BeautifulSoup(req.content, 'html.parser')
    json_ld_data = render_json_ltd(link, req.text)
    page = metadata_parser.MetadataParser(
        url=link,
        url_headers=headers,
        search_head_only=False
    )
    card = ["bookmark", {
                "type": "bookmark",
                "url": get_canonical(page),
                "metadata": {
                    "url": get_canonical(page),
                    "title": get_title(page, json_ld_data),
                    "description": get_description(page, json_ld_data),
                    "author": get_author(page, html, json_ld_data),
                    "publisher": get_publisher(json_ld_data),
                    "thumbnail": get_image(page, json_ld_data),
                    "icon": get_favicon(page, html, json_ld_data, get_domain(link))
                    }
                }
            ]
    return card


def render_json_ltd(link, html):
    """Fetch structured data."""
    json_ld_data = extruct.extract(
        str(html),
        base_url=get_domain(link),
        syntaxes=['json-ld'],
        uniform=True)['json-ld']
    if len(json_ld_data) >= 1:
        json_ld_data = json_ld_data[0]
    return json_ld_data


def get_title(page, json_ld_data):
    """Scrape page title."""
    title = None
    if bool(json_ld_data) and json_ld_data.get('title'):
        title = json_ld_data['title']
    elif bool(json_ld_data) and json_ld_data.get('headline'):
        title = json_ld_data['headline']
    elif page.get_metadatas('title'):
        title = page.get_metadatas('title')
    elif page.get_metadatas('og:title'):
        title = page.get_metadatas('og:title')
    elif page.get_metadatas('twitter:title'):
        title = page.get_metadatas('twitter:title')
    if title:
        title = title[0].split('|')[0]
    return title


def get_image(page, json_ld_data):
    """Scrape page `share image`."""
    image = None
    if bool(json_ld_data) and json_ld_data.get('image'):
        image = json_ld_data['image'].get('url')
    elif page.get_metadatas('og:image'):
        image = page.get_metadatas('og:image')[0]
    elif page.get_metadatas('twitter:image'):
        image = page.get_metadatas('twitter:image')[0]
    return image


def get_description(page, json_ld_data):
    """Scrape page description."""
    description = None
    if bool(json_ld_data) and json_ld_data.get('description'):
        description = json_ld_data['description']
    elif page.get_metadatas('description'):
        description = page.get_metadatas('description')[0]
    elif page.get_metadatas('og:description'):
        description = page.get_metadatas('og:description')[0]
    elif page.get_metadatas('twitter:description'):
        description = page.get_metadatas('twitter:description')[0]
    return description


def get_author(page, html, json_ld_data):
    """Scrape author name."""
    author = None
    if bool(json_ld_data):
        if type(json_ld_data['author']) == list:
            json_ld_author = json_ld_data['author'][0]
            author = json_ld_author.get('name')
        elif type(json_ld_data['author']) == dict:
            author = json_ld_data['author'].get('name')
    elif page.get_metadatas('author'):
        author = page.get_metadatas('author')[0]
    elif page.get_metadatas('article:author'):
        author = page.get_metadatas('article:author')[0]
    elif page.get_metadatas('twitter:creator'):
        author = page.get_metadatas('twitter:creator')[0]
    elif html.find("a", attrs={"class": "commit-author"}):
        author = html.find("a", attrs={"class": "commit-author"}).get('href')
    return author


def get_publisher(json_ld_data):
    """Scrape publisher name."""
    publisher = None
    if bool(json_ld_data):
        if type(json_ld_data['publisher']) == list:
            json_ld_publisher = json_ld_data['publisher'][0]
            publisher = json_ld_publisher.get('name')
        elif type(json_ld_data['publisher']) == dict:
            publisher = json_ld_data['publisher'].get('name')
    return publisher


def get_favicon(page, html, json_ld_data, base_url):
    """Scrape favicon image."""
    favicon = None
    if bool(json_ld_data) and json_ld_data.get('logo'):
        favicon = json_ld_data['logo'].get('url')
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
    if favicon and favicon[0] == '/':
        favicon = base_url + favicon
    if favicon and favicon[0] != 'h':
        favicon = base_url + '/' + favicon
    if favicon is None:
        favicon = base_url + 'favicon.ico'
    return favicon


def get_domain(url):
    """Get site root domain name."""
    domain = url.split('//')[1]
    name = domain.split('/')[0]
    return f'https://{name}/'


def get_canonical(page):
    """Get page canonical URL."""
    canonical = None
    if page.get_metadatas('canonical'):
        canonical = page.get_metadatas('canonical')[0]
    return canonical
