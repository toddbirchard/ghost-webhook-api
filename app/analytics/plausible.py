"""Fetch site analytics via Plausible API."""
from typing import List, Optional, Tuple

import requests
from requests.exceptions import RequestException

from clients import ghost
from config import settings
from log import LOGGER


def fetch_top_visited_posts(time_period: str, limit=20) -> Tuple[int, List[Optional[dict]]]:
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
            "limit": limit,
        }
        resp = requests.get(
            settings.PLAUSIBLE_BREAKDOWN_ENDPOINT,
            params=params,
            headers=headers,
        )
        if resp.status_code == 200:
            results_list = resp.json().get("results")
            results_list = filter_pages_from_post_results(results_list)
            if results_list:
                visited_posts = enrich_url_with_post_data(results_list)
                num_visited_posts = aggregate_total_hits(visited_posts)
                if num_visited_posts > 0:
                    LOGGER.warning(f"num_visited_posts: {num_visited_posts} | visited_posts: {visited_posts}")
                    return num_visited_posts, visited_posts
                return 0, []
    except RequestException as e:
        LOGGER.error(f"RequestException when fetching Plausible top URLs: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected Exception when fetching Plausible top URLs: {e}")


def filter_pages_from_post_results(results_list: dict) -> List[dict]:
    """
    Ensure all analytics results are for posts, not pages.

    :param dict results_list: JSON response of top-visited pages.

    :returns: List[dict]
    """
    # NOTE: This is a shit show.
    page_slugs = [page["slug"] for page in ghost.get_pages()]
    # for slug in page_slugs:
        # LOGGER.warning(f"slug: {slug}")
    return [
        result
        for result in results_list
        if "/tag" not in result["page"]
        and "/page" not in result["page"]
        and "/author" not in result["page"]
        and "/series" not in result["page"]
        and "/about" not in result["page"]
        and "/build-flask-apps" not in result["page"]
        and "/python-concurrency-with-asyncio" not in result["page"]
        and "/hacking-tableau-server" not in result["page"]
        and "/intro-to-asyncio-concurrency" not in result["page"]
        and "/" != result["page"]
        and result["page"] not in page_slugs
        and result["page"] is not None
    ]


def enrich_url_with_post_data(results: dict) -> Optional[dict]:
    """
    Determine post slug from URL & fetch Ghost post title.

    :param dict page_result: `Top visited URLs` result returned by Plausible.

    :returns: Optional[dict]
    """
    slug = [result["page"].rstrip("/").lstrip("/").split("/")[-1] for result in results]
    post = ghost.get_post_by_slug(slug)
    if post is not None:
        post["slug"] = slug
        post["title"] = post["title"]
        post["url"] = post["url"]
        return post
    return None


def aggregate_total_hits(visited_posts: List[dict]) -> int:
    """
    Get total number of visits to site.

    :param List[dict] visited_posts: List of top visited posts.

    :returns: int
    """
    return sum([page.get("visitors", 0) for page in visited_posts])
