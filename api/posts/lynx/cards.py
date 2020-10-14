"""Replace <a> tags in Lynx posts with cards."""
from typing import List
import re
import simplejson as json
import requests
from clients.log import LOGGER
from api.posts.lynx.utils import http_headers
from .scrape import scrape_link
from .doc import mobile_doc


@LOGGER.catch
def generate_link_previews(post: dict) -> str:
    """Replace <a> tags in Lynx posts with link previews."""
    html = post.get('html')
    urls = re.findall('<a href="(.*?)"', html)
    links = remove_404s(urls)
    link_previews = [scrape_link(link) for link in links if link is not None]
    mobile_doc['cards'] = link_previews
    for i, link in enumerate(link_previews):
        mobile_doc['sections'].append([10, i])
    return json.dumps(mobile_doc)


@LOGGER.catch
def remove_404s(links: List[str]) -> List[str]:
    """Remove links which result in 404s."""
    valid_links = []
    for link in links:
        res = requests.get(link, headers=http_headers)
        if res.status_code == 200:
            valid_links.append(link)
    return valid_links

