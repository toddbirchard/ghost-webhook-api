"""Replace <a> tags in Lynx posts with cards."""
import re
from typing import List

import requests
from flask import render_template

from api.posts.lynx.mobiledoc import mobile_doc
from api.posts.lynx.scrape import scrape_link
from api.posts.lynx.utils import http_headers
from clients.log import LOGGER


@LOGGER.catch
def generate_link_previews(post: dict) -> str:
    """Replace <a> tags in Lynx posts with link previews."""
    html = post.get("html")
    urls = re.findall('<a href="(.*?)"', html)
    links = remove_404s(urls)
    link_previews = [scrape_link(link) for link in links if link is not None]
    mobile_doc["cards"] = link_previews
    for i, link in enumerate(link_previews):
        mobile_doc["sections"].append([10, i])
    return mobile_doc
    # return json.dumps(mobile_doc)


def generate_bookmark_html(html: str) -> str:
    urls = re.findall('<a href="(.*?)"', html)
    links = remove_404s(urls)
    link_previews = [scrape_link(link) for link in links if link is not None]
    card_html = []
    for i, link in enumerate(link_previews):
        card_html.append(
            render_template(
                "bookmark.jinja2",
                title=link[1]["metadata"]["title"],
                description=link[1]["metadata"]["description"],
                url=link[1]["url"],
                author=link[1]["metadata"]["author"],
                icon=link[1]["metadata"]["icon"],
                publisher=link[1]["metadata"]["publisher"],
                image=link[1]["metadata"]["image"],
            )
        )
    card_html_string = "".join(card_html)
    # LOGGER.info(card_html_string)
    return card_html_string


@LOGGER.catch
def remove_404s(links: List[str]) -> List[str]:
    """Remove links which result in 404s."""
    valid_links = []
    for link in links:
        res = requests.get(link, headers=http_headers)
        if res.status_code == 200:
            valid_links.append(link)
    return valid_links
