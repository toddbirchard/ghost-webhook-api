"""Fetch site analytics via Plausible API."""
from typing import List, Optional

import requests
from fastapi import HTTPException
from requests.exceptions import RequestException

from clients import ghost
from config import settings
from log import LOGGER


def top_visited_pages_by_timeframe(time_period: str, limit=30) -> Optional[List[dict]]:
    """
    Get top visited URLs & enrich with post metadata.

    :param str time_period: Period of time to fetch results for (12mo, 6mo, month, 30d, 7d, or day).
    :param int limit: Maximum number of results to be returned.

    :returns: List[Optional[dict]]
    """
    results = fetch_top_visited_pages(time_period, limit=limit)
    if results:
        results = filter_results(results)
        results = enrich_results(results)
        return results
    return []


def fetch_top_visited_pages(time_period: str, limit=30) -> List[Optional[dict]]:
    """
    Fetch top visited URLs from Plausible.

    :param str time_period: Period of time to fetch results for (12mo, 6mo, month, 30d, 7d, or day).
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
            "metrics": "visitors,bounce_rate,visitors,pageviews,visit_duration",
            "property": "event:page",
        }
        resp = requests.get(
            settings.PLAUSIBLE_STATS_ENDPOINT,
            params=params,
            headers=headers,
        )
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Failed to fetch Plausible results for time period of `{time_period}` : {resp.text}.",
            )
        return resp.json().get("results")
    except RequestException as e:
        LOGGER.error(f"RequestException when fetching Plausible top URLs: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected Exception when fetching Plausible top URLs: {e}")


def fetch_all_ghost_urls() -> List[dict]:
    """
    List all slugs for Ghost posts & pages.

    :returns: List[dict]
    """
    ghost_pages = ghost.get_pages()
    return [f"/{page.get('slug')}/" for page in ghost_pages if page.get("slug") is not None and page is not None]


def filter_results(results_list: List[dict]) -> List[dict]:
    """
    Fetch all Ghost posts & filter unimportant pages.

    :param List[dict] results_list: List of top visited URLs.

    :returns: List[dict]
    """
    ghost_page_urls = fetch_all_ghost_urls()
    return [
        result
        for result in results_list
        if result is not None
        and result.get("pageviews") is not None
        and result["pageviews"] > 6
        and "/tag" not in result["page"]
        and "/page" not in result["page"]
        and "/author" not in result["page"]
        and "/series" not in result["page"]
        and result["page"] != "about"
        and result["page"] != "/"
        and result["page"] != ""
        and result["page"] not in ghost_page_urls
    ]


def enrich_url_with_post_data(page_result: dict) -> Optional[dict]:
    """
    Determine post slug from URL & fetch Ghost post title.

    :param dict page_result: Top visited URL result returned by Plausible.

    :returns: Optional[dict]
    """
    slug = page_result["page"].rstrip("/").lstrip("/").split("/")[-1]
    post = ghost.get_post_by_slug(slug)
    if post and page_result["pageviews"] and page_result["pageviews"] > 2:
        page_result["slug"] = slug
        page_result["title"] = post["title"]
        page_result["url"] = f"{post['url']}"
        return page_result
    return None


def enrich_results(results: List[dict]):
    """
    Add additional Ghost page metadata to Plausible results.

    :param List[dict] results:

    :returns: List[dict]
    """
    return [enrich_url_with_post_data(result) for result in results if result is not None]
