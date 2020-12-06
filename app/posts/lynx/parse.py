"""Replace <a> tags in Lynx posts with cards."""
import re
from typing import List

import requests
import simplejson as json
from requests.exceptions import HTTPError, SSLError

from app.posts.lynx.mobiledoc import mobile_doc
from app.posts.lynx.scrape import scrape_link
from clients.log import LOGGER
from config import basedir
from database import rdbms


@LOGGER.catch
def generate_link_previews(post: dict) -> (int, str):
    """Replace <a> tags in Lynx posts with link previews."""
    new_mobiledoc = mobile_doc
    html = post["html"]
    urls = re.findall('<a href="(.*?)"', html)
    links = remove_404s(urls)
    if links is not None:
        link_previews = [scrape_link(link) for link in links if link is not None]
        new_mobiledoc["cards"] = link_previews
        for i, link in enumerate(link_previews):
            new_mobiledoc["sections"].append([10, i])
        return len(link_previews), json.dumps(new_mobiledoc).replace("\n", "")
    return 0, post["mobiledoc"]


@LOGGER.catch
def remove_404s(links: List[str]) -> List[str]:
    """Remove links which result in 404s."""
    http_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }
    valid_links = []
    for link in links:
        try:
            res = requests.get(link, headers=http_headers)
            if res.status_code == 200:
                valid_links.append(link)
        except SSLError as e:
            LOGGER.error(e)
            pass
        except HTTPError as e:
            LOGGER.error(e)
            pass
        except Exception as e:
            LOGGER.error(e)
            pass
    return valid_links


def batch_lynx_embeds() -> (int, List[dict]):
    total_embeds = 0
    updated_posts = []
    sql_file = open(f"{basedir}/app/posts/queries/selects/lynx_bookmarks.sql", "r")
    query = sql_file.read()
    posts = rdbms.execute_query(query, "hackers_prod").fetchall()
    for post in posts:
        post_id = post["id"]
        post_title = post["title"]
        num_links, doc = generate_link_previews(post)
        total_embeds += num_links
        rdbms.execute_query(
            f"UPDATE posts SET mobiledoc = '{doc}' WHERE id = '{post_id}';",
            "hackers_prod",
        )
        updated_posts.append({post_title: f"{num_links} link embeds created."})
    return total_embeds, updated_posts
