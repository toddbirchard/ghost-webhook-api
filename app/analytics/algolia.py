"""Helper functions to fetch search query activity from Algolia."""
from typing import List, Optional

import requests
from requests.exceptions import HTTPError

from app.moment import get_current_date
from clients.log import LOGGER
from config import Settings


def fetch_algolia_searches(timeframe: int = 7) -> Optional[List[str]]:
    """
    Fetch single week of searches from Algolia API.

    :timeframe: Number of days for which to fetch recent search analytics.
    :type timeframe: int
    """
    endpoint = f"{Settings().ALGOLIA_BASE_URL}/searches"
    headers = {
        "x-algolia-application-id": Settings().ALGOLIA_APP_ID,
        "x-algolia-api-key": Settings().ALGOLIA_API_KEY,
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


def filter_results(search_queries: list) -> List[Optional[str]]:
    """
    Filter noisy or irrelevant search analytics from results (ie: too short).

    :param search_queries: Search analytics submitted by users while searching for posts.
    :type search_queries: List[str]

    :returns: List[Optional[str]]
    """
    search_queries = [query["search"].strip() for query in search_queries]
    search_queries = list(filter(lambda x: len(x["search"]) > 3, search_queries))
    return search_queries
