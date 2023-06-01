"""Helper functions to fetch search query activity from Algolia."""
from typing import Any, Dict, List, Optional

import requests
from fastapi import HTTPException
from requests.exceptions import HTTPError

from app.moment import get_start_date_range
from config import settings
from database import feature_db
from log import LOGGER


def persist_algolia_searches(time_period: str) -> List[Optional[dict]]:
    """
    Fetch single week of searches from Algolia API.

    :param str time_period: Period of time for which to fetch search queries (7d, 30d, month, 12mo).
    :param str db_table: DB table name

    :returns: List[Optional[dict]]
    """
    try:
        headers = {
            "x-algolia-application-id": settings.ALGOLIA_APP_ID,
            "x-algolia-api-key": settings.ALGOLIA_API_KEY,
        }
        params = {
            "index": "hackers_posts",
            "limit": 999999,
            "orderBy": "searchCount",
            "direction": "desc",
            "startDate": get_start_date_range(time_period),
        }
        resp = requests.get(settings.ALGOLIA_SEARCHES_ENDPOINT, headers=headers, params=params)
        if resp.status_code == 200 and resp.json().get("searches") is not None:
            search_queries = resp.json().get("searches")
            search_queries = filter_search_queries(search_queries)
            if search_queries is not None:
                import_algolia_search_queries(search_queries, time_period)
                return search_queries
            return []
        return []
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching Algolia searches for `{time_period}`: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching Algolia searches for `{time_period}`: {e}")


def fetch_algolia_searches(time_period: str) -> List[Optional[dict]]:
    """
    Fetch analytics from Algolia API for a given time period.

    :param str time_period: Period of time for which to fetch search queries (7d, 30d, month, 12mo).

    :returns: List[Optional[dict]]
    """
    try:
        headers = {
            "x-algolia-application-id": settings.ALGOLIA_APP_ID,
            "x-algolia-api-key": settings.ALGOLIA_API_KEY,
        }
        params = {
            "index": "hackers_posts",
            "limit": 999999,
            "orderBy": "searchCount",
            "direction": "desc",
            "startDate": get_start_date_range(time_period),
        }
        resp = requests.get(settings.ALGOLIA_SEARCHES_ENDPOINT, headers=headers, params=params)
        if resp.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch Algolia results for `{time_period}` time period: {resp.text}.",
            )
        resp.json().get("searches")
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching Algolia searches for `{time_period}`: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching Algolia searches for `{time_period}`: {e}")


def filter_search_queries(search_queries: List[Dict[str, Any]]) -> List[Optional[Dict[str, Any]]]:
    """
    Filter noisy or irrelevant search analytics from results (ie: too short).

    :param search_queries: JSON of search queries submitted by users.
    :type search_queries: List[Optional[Dict[str, Any]]]

    :returns: List[Dict[str, Any]]
    """
    return [query for query in search_queries if len(query["search"]) > 3]


def import_algolia_search_queries(records: List[dict], table_name: str) -> Optional[List[dict]]:
    """
    Save history of search queries executed on the site.

    :param List[dict] records: JSON of search queries submitted by users.
    :param str table_name: Name of SQL table to save data to.

    :returns: Optional[List[dict]]
    """
    return feature_db.insert_records(
        records,
        table_name,
        replace=True,
    )
