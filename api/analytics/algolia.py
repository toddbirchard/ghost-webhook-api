"""Fetch posts from Algolia REST API."""
from typing import List, Optional

import requests
from flask import current_app as api
from requests.exceptions import HTTPError

from api.moment import get_current_date
from clients.log import LOGGER


def fetch_algolia_searches(timeframe=7) -> Optional[List[str]]:
    """Fetch single week of searches from Algolia API."""
    endpoint = f'{api.config["ALGOLIA_BASE_URL"]}/searches'
    headers = {
        "x-algolia-application-id": api.config["ALGOLIA_APP_ID"],
        "x-algolia-api-key": api.config["ALGOLIA_API_KEY"],
    }
    params = {
        "index": "hackers_posts",
        "limit": 999999,
        "startDate": get_current_date(timeframe),
    }
    try:
        req = requests.get(endpoint, headers=headers, params=params)
        search_queries = req.json()["searches"]
        return filter_results(search_queries)
    except HTTPError as e:
        LOGGER.error(f"Failed to fetch Algolia searches: {e}")
        return None
    except KeyError as e:
        LOGGER.error(f"Experienced KeyError while fetching Algolia searches: {e}")
        return None
    except Exception as e:
        LOGGER.error(
            f"Experienced unexpected error while fetching Algolia searches: {e}"
        )
        return None


def filter_results(search_queries: list) -> list:
    """Filter garbage search queries."""
    search_queries = list(filter(lambda x: len(x["search"]) > 2, search_queries))
    search_queries = list(
        filter(lambda x: x["search"].replace(" ", "") != "", search_queries)
    )
    return search_queries
