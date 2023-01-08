"""Fetch site analytics via Plausible API."""
from typing import List, Optional

import requests
from requests.exceptions import RequestException

from clients import ghost
from config import settings
from log import LOGGER


def fetch_top_visited_urls(time_period: str, limit=20) -> List[Optional[dict]]:
    """
    Fetch top visited URLs from Plausible.

    :param str time_period: Period of 12mo, 6mo, month, 30d, 7d, or day.
    :param int limit: Maximum number of results to be returned.

    :returns: Optional[List[dict]]
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.PLAUSIBLE_API_TOKEN}",
        }
        params = {
            "site_id": "hackersandslackers.com",
            "period": time_period,
            "property": "event:page",
            "metrics": "visitors,bounce_rate",
            "limit": limit,
        }
        resp = requests.get(
            settings.PLAUSIBLE_BREAKDOWN_ENDPOINT,
            auth=f"Bearer {settings.PLAUSIBLE_API_TOKEN}",
            params=params,
            headers=headers,
        )
        if resp.status_code == 200:
            results_list = resp.json().get("results")
            if results_list:
                return format_top_visited_urls(results_list)
        return []
    except RequestException as e:
        LOGGER.error(f"RequestException when fetching Plausible top URLs: {e}")
        return []
    except Exception as e:
        LOGGER.error(f"Unexpected Exception when fetching Plausible top URLs: {e}")
        return []


def format_top_visited_urls(results_list: List[Optional[dict]]) -> List[Optional[dict]]:
    """
    Format top visited URLs for Slack message.

    :param List[dict] urls: List of top visited URLs.

    :returns: str
    """
    if results_list:
        ghost_posts = [f"/{page['slug']}/" for page in ghost.get_pages()]
        results_list = [
            result
            for result in results_list
            if "/tag" not in result["page"]
            and "/page" not in result["page"]
            and "/author" not in result["page"]
            and "/series" not in result["page"]
            and "/about" not in result["page"]
            and result["page"] not in ghost_posts
        ]
        if results_list:
            return [enrich_url_with_post_data(result) for result in results_list if result is not None]
    return []


def enrich_url_with_post_data(page_result: dict) -> Optional[dict]:
    """
    Determine post slug from URL & fetch Ghost post title.

    :param dict page_result: Top visited URL result returned by Plausible.

    :returns: Optional[dict]
    """
    post_json = {}
    slug = page_result["page"].rstrip("/").lstrip("/").split("/")[-1]
    if slug:
        post = ghost.get_post_by_slug(slug)
        if post is not None:
            post_json["slug"] = slug
            post_json["title"] = post["title"]
            post_json["url"] = f"{post['url']}"
        return post_json
    return None
