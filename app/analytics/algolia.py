"""Helper functions to fetch search query activity from Algolia."""
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import HTTPError

from app.moment import get_start_date_range
from config import settings
from database import rdbms
from log import LOGGER


def fetch_algolia_searches(table_name: str, timeframe: int) -> Optional[List[dict]]:
    """
    Fetch single week of searches from Algolia API.

    :param timeframe: Number of days for which to fetch recent search analytics.
    :param str table_name: DB table name

    :returns: Optional[List[dict]]
    """
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
    try:
        req = requests.get(endpoint, headers=headers, params=params)
        search_queries = req.json()["searches"]
        search_queries = filter_search_queries(search_queries)
        return import_algolia_search_queries(search_queries, table_name)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching Algolia searches: {e}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching Algolia searches: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching Algolia searches: {e}")


def filter_search_queries(
    search_queries: List[Dict[str, Any]]
) -> List[Optional[Dict[str, Any]]]:
    """
    Filter noisy or irrelevant search analytics from results (ie: too short).

    :param search_queries: JSON of search queries submitted by users.
    :type search_queries: List[Optional[Dict[str, Any]]]

    :returns: List[Dict[str, Any]]
    """
    return [query for query in search_queries if len(query["search"]) < 3]


def import_algolia_search_queries(records: List[dict], table_name: str) -> str:
    """
    Save history of search queries executed on the site.

    :param List[dict] records: JSON of search queries submitted by users.
    :param str table_name: Name of SQL table to save data to.

    :returns: str
    """
    replace = True
    if table_name == "algolia_searches_historical":
        replace = False
    result = rdbms.insert_records(
        records,
        table_name,
        "analytics",
        replace=replace,
    )
    LOGGER.success(f"Inserted {len(result)} rows into `{table_name}` table.")
    return result
