"""Helper functions to fetch search query activity from Algolia."""
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import HTTPError

from app.moment import get_current_date
from clients.log import LOGGER
from config import settings


def fetch_algolia_searches(timeframe: int = 7) -> Optional[List[str]]:
    """
    Fetch single week of searches from Algolia API.

    :timeframe: Number of days for which to fetch recent search analytics.
    :type timeframe: int
    """
    endpoint = f"{settings.ALGOLIA_BASE_URL}/searches"
    headers = {
        "x-algolia-application-id": settings.ALGOLIA_APP_ID,
        "x-algolia-api-key": settings.ALGOLIA_API_KEY,
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


def filter_results(
    search_queries: List[Optional[Dict[str, Any]]]
) -> List[Optional[str]]:
    """
    Filter noisy or irrelevant search analytics from results (ie: too short).

    :param search_queries: Search analytics submitted by users while searching for posts.
    :type search_queries: List[str]

    :returns: List[Optional[str]]
    """
    search_queries = [query for query in search_queries if len(query["search"]) > 3]
    return search_queries
