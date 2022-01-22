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

    :param str url: Link to third-party content, for which to create a link preview.

    :returns: Optional[List[dict]]
    """
    try:
        # Parse page metadata as dict
        page = MetadataParser(
            url=url, url_headers=headers, ssl_verify=True, search_head_only=True
        )
        page_meta = page.metadata["meta"]
        # Return regular bookmark or Twitter card depending on source
        if "twitter.com" in url:
            return create_twitter_card(url)
        return create_bookmark_card(page, page_meta, url)
    except HTTPError as e:
        LOGGER.warning(f"Failed to fetch metadata for URL `{url}`: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while scraping metadata for URL `{url}`: {e}")


def create_bookmark_card(page: MetadataParser, page_meta: dict, url: str) -> List[dict]:
    """
    Create a preview bookmark card from a URL.

    :param MetadataParser page: Page object create from URL to be parsed.
    :param dict page_meta: Page metadata parsed from the head of the target URL.
    :param str url: URL of the linked third-party post/article.

    :returns: Optional[List[dict]]
    """
    try:
        author = page_meta.get("author")
        publisher = page_meta.get("publisher")
        icons = page.soup.select("link[rel=icon]")
        bookmark = [
            "bookmark",
            {
                "type": "bookmark",
                "url": url,
                "metadata": {
                    "url": url,
                    "title": page_meta.get("og:title"),
                    "description": page_meta.get("og:description"),
                    "image": page.get_metadata_link(
                        "image", allow_encoded_uri=True, require_public_global=True
                    ),
                },
            },
        ]
        if author:
            bookmark[1]["metadata"]["author"] = author
        if publisher:
            bookmark[1]["metadata"]["publisher"] = publisher
        if icons:
            bookmark[1]["metadata"]["icon"] = url + icons[0].attrs["href"]
        return bookmark
    except Exception as e:
        LOGGER.error(f"Unexpected error while generating Bookmark card: {e}")


def create_twitter_card(url: str) -> Optional[List[dict]]:
    """
    Create a Twitter embed card from dangling Twitter URL.

    :param str url: URL of the linked Twitter post.

    :returns: Optional[List[dict]]
    """
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
