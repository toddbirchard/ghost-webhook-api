"""Scrape URLs found in body of Lynx posts for metadata."""
from typing import List, Optional

import requests
from metadata_parser import MetadataParser
from requests.exceptions import HTTPError

from log import LOGGER

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


def scrape_metadata_from_url(url: str) -> Optional[List[dict]]:
    """
    Fetch metadata for a given URL.

    :param str url:

    """
    try:
        # Parse page metadata as dict
        page = MetadataParser(url=url, url_headers=headers, ssl_verify=True)
        page_meta = page.fetch_url()["page"]
        # Return regular bookmark or Twitter card depending on source
        if "twitter.com" in url:
            return create_twitter_card(url)
        else:
            create_bookmark_card(page, page_meta, url)
    except HTTPError as e:
        LOGGER.warning(f"Failed to fetch metadata for URL `{url}`: {e}")


def create_bookmark_card(page, page_meta: dict, url: str) -> List[dict]:
    try:
        return [
            "bookmark",
            {
                "type": "bookmark",
                "url": url,
                "metadata": {
                    "url": url,
                    "title": page_meta.get("title"),
                    "description": page_meta.get("description"),
                    "author": page_meta.get("author"),
                    "publisher": page_meta.get("publisher"),
                    "image": page.get_metadata_link(
                        "image", allow_encoded_uri=True, require_public_global=True
                    ),
                    "icon": page_meta.get("icon"),
                },
            },
        ]
    except Exception as e:
        LOGGER.error(f"Unexpected Error while generating Bookmark card: {e}")


def create_twitter_card(url: str) -> Optional[List[dict]]:
    try:
        req = requests.get(f"https://publish.twitter.com/oembed?url={url}")
        if req.status_code == 200:
            tweet = req.json()
            card = [
                "embed",
                {
                    "url": tweet.get("url"),
                    "html": tweet.get("html"),
                    "type": "rich",
                    "metadata": {
                        "url": tweet.get("url"),
                        "author_name": tweet.get("author_name"),
                        "author_url": tweet.get("author_url"),
                        "width": 550,
                        "height": None,
                        "cache_age": "3153600000",
                        "provider_name": "Twitter",
                        "provider_url": "http://www.twitter.com/",
                        "version": "1.0",
                    },
                },
            ]
            return card
    except HTTPError as e:
        LOGGER.error(f"HTTP Error while generating Twitter card: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected Error while generating Twitter card: {e}")
