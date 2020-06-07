"""Parse individual Lynx URLs."""
import requests
import metadata_parser
from bs4 import BeautifulSoup
import extruct
from api.log import LOGGER


@LOGGER.catch
def scrape_link(link):
    """Get link metadata."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(link, headers=headers)
    html = BeautifulSoup(req.content, 'html.parser')
    json_ld_data = render_json_ltd(link, req.text)
    page = metadata_parser.MetadataParser(url=link, url_headers=headers, search_head_only=False)
    card = ["bookmark", {
                "type": "bookmark",
                "url": get_canonical(page),
                "metadata": {
                    "url": get_canonical(page),
                    "title": get_title(page),
                    "description": get_description(page),
                    "author": get_author(page, html, json_ld_data),
                    "publisher": get_publisher(json_ld_data),
                    "thumbnail": get_image(page),
                    "icon": get_favicon(page, html, get_domain(link))
                    }
                }]
    return card


def render_json_ltd(link, html):
    json_ld_data = extruct.extract(
        str(html),
        base_url=get_domain(link),
        syntaxes=['json-ld'],
        uniform=True)['json-ld']
    if len(json_ld_data) >= 1:
        json_ld_data = json_ld_data[0]
    return json_ld_data


def get_title(page):
    """Attempt to get a title."""
    title = None
    if page.get_metadatas('title'):
        title = page.get_metadatas('title')
    elif page.get_metadatas('og:title'):
        title = page.get_metadatas('og:title')
    elif page.get_metadatas('twitter:title'):
        title = page.get_metadatas('twitter:title')
    if title:
        title = title[0].split('|')[0]
    return title


def get_image(page):
    """Attempt to get a title."""
    image = None
    if page.get_metadatas('og:image'):
        image = page.get_metadatas('og:image')[0]
    elif page.get_metadatas('twitter:image'):
        image = page.get_metadatas('twitter:image')[0]
    return image


def get_description(page):
    """Attempt to get description."""
    description = None
    if page.get_metadatas('description'):
        description = page.get_metadatas('description')[0]
    elif page.get_metadatas('og:description'):
        description = page.get_metadatas('og:description')[0]
    elif page.get_metadatas('twitter:description'):
        description = page.get_metadatas('twitter:description')[0]
    return description


def get_author(page, html, json_ld_data):
    """Scrape author name."""
    author = None
    if page.get_metadatas('author'):
        author = page.get_metadatas('author')[0]
    elif page.get_metadatas('article:author'):
        author = page.get_metadatas('article:author')[0]
    elif page.get_metadatas('twitter:creator'):
        author = page.get_metadatas('twitter:creator')[0]
    elif html.find("a", attrs={"class": "commit-author"}):
        author = html.find("a", attrs={"class": "commit-author"}).get('href')
    elif bool(json_ld_data) and json_ld_data.get('author'):
        author = json_ld_data['author'].get('name')
    return author


def get_publisher(json_ld_data):
    """Scrape author name."""
    publisher = None
    if bool(json_ld_data) and json_ld_data.get('publisher'):
        publisher = json_ld_data['publisher'].get('name')
    return publisher


def get_favicon(page, html, base_url):
    """Attempt to get favicon."""
    favicon = None
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
    """Get canonical URL."""
    canonical = None
    if page.get_metadatas('canonical'):
        canonical = page.get_metadatas('canonical')[0]
    return canonical
