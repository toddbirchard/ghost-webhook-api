"""Helper functions to fetch search query activity from Algolia."""
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import HTTPError

from app.moment import get_start_date_range
from config import settings
from database import rdbms
from log import LOGGER


def fetch_algolia_searches(table_name: str, timeframe: int) -> List[Optional[dict]]:
    """
    Fetch single week of searches from Algolia API.

    :param timeframe: Number of days for which to fetch recent search analytics.
    :param str table_name: DB table name

    :returns: List[Optional[dict]]
    """
    try:
        endpoint = "https://analytics.algolia.com/2/searches"
        headers = {
            "x-algolia-application-id": settings.ALGOLIA_APP_ID,
            "x-algolia-api-key": settings.ALGOLIA_API_KEY,
        }
        params = {
            "index": "hackers_posts",
            "limit": 999999,
            "startDate": get_start_date_range(timeframe),
        }
        resp = requests.get(endpoint, headers=headers, params=params)
        if resp.status_code == 200 and resp.json().get("searches") is not None:
            search_queries = resp.json().get("searches")
            search_queries = filter_search_queries(search_queries)
            if search_queries is not None:
                import_algolia_search_queries(search_queries, table_name)
                return search_queries
            return []
        return []
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching Algolia searches for `{timeframe}`: {e}"
        )
    except ValueError as e:
        LOGGER.error(
            f"ValueError while fetching Algolia searches for `{timeframe}`: {e}"
        )
    except Exception as e:
        LOGGER.error(
            f"Unexpected error while fetching Algolia searches for `{timeframe}`: {e}"
        )


def filter_search_queries(
    search_queries: List[Dict[str, Any]]
) -> List[Optional[Dict[str, Any]]]:
    """
    Filter noisy or irrelevant search analytics from results (ie: too short).

    :param search_queries: JSON of search queries submitted by users.
    :type search_queries: List[Optional[Dict[str, Any]]]

    :returns: List[Dict[str, Any]]
    """
    return [query for query in search_queries if len(query["search"]) > 3]


def import_algolia_search_queries(
    records: List[dict], table_name: str
) -> Optional[List[dict]]:
    """
    Save history of search queries executed on the site.

    :param List[dict] records: JSON of search queries submitted by users.
    :param str table_name: Name of SQL table to save data to.

    :returns: Optional[List[dict]]
    """
    replace = True
    if table_name == "algolia_searches_historical":
        replace = False
    return rdbms.insert_records(
        records,
        table_name,
        "analytics",
        replace=replace,
    )
