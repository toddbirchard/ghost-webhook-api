"""Fetch site analytics via Plausible API."""
from typing import List, Optional

import requests
from fastapi import HTTPException
from requests.exceptions import RequestException

from clients import ghost
from config import settings
from database.schemas import PostInsight
from log import LOGGER


def top_visited_pages_by_timeframe(time_period: str, limit=50) -> List[Optional[PostInsight]]:
    """
    Fetch most-visited URLs from Plausible, filter non-post results, and enrich with metadata.

    :param str time_period: Period of time to fetch results for (12mo, 6mo, month, 30d, 7d, or day).
    :param int limit: Maximum number of results to be returned.

    :returns: List[Optional[dict]]
    """
    results = fetch_top_visited_pages(time_period, limit=limit)
    if results:
        results = filter_results(results)
        results = build_post_insight_objects(results)
        return results
    return []


def fetch_top_visited_pages(time_period: str, limit=50) -> List[Optional[dict]]:
    """
    Fetch parent site's top-visited URLs from Plausible API.

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


def fetch_all_ghost_page_urls() -> List[dict]:
    """
    Fetch all slugs for Ghost static pages; used to filter non-posts.

    :returns: List[dict]
    """
    ghost_pages = ghost.get_all_pages()
    return [{page.get("url")} for page in ghost_pages if page.get("url")]


def filter_results(results_list: List[dict]) -> List[dict]:
    """
    Filter non-posts from results list, as well as low-performing posts.

    :param List[dict] results_list: List of top visited URLs.

    :returns: List[dict]
    """
    ghost_page_urls = fetch_all_ghost_page_urls()
    return [
        result
        for result in results_list
        if result is not None
        and result.get("pageviews") is not None
        and result["pageviews"] > 6
        and result["page"] not in ghost_page_urls
        and "/series/" not in result["page"]
        and "/about/" not in result["page"]
        and "/tag/" not in result["page"]
        and "/author/" not in result["page"]
        and "/404/" not in result["page"]
        and result["page"] != "/"
        and result["page"] != "/managing-user-session-variables-with-flask-sessions-and-redis/"
    ]


def build_post_insight_objects(results: List[dict]) -> List[Optional[PostInsight]]:
    """
    Construct an object to represent post's insight object & enrich record with matching Ghost data.

    :param List[dict] result: Raw Plausible records each representing a "top-visited" URL result.

    :returns: List[Optional[PageInsight]]
    """
    page_insights = []
    for result in results:
        slug = result["page"].rstrip("/").lstrip("/").split("/")[-1]
        post = ghost.get_post_by_slug(slug)
        if post and result and result["pageviews"] and result["pageviews"] > 2 and post["slug"] == slug:
            page_insight = PostInsight(
                page_views=result["pageviews"],
                unique_visitors=result["visit_duration"],
                avg_visit_duration_secs=result["visit_duration"],
                bounce_rate_pct=post["title"],
                title=post["title"],
                slug=post["slug"],
                url=f"{post['url']}",
            )
            page_insights += page_insight
    return page_insights
