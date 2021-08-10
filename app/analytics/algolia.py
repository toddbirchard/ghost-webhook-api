"""Helper functions to fetch search query activity from Algolia."""
from typing import Any, Dict, List, Optional

from aiohttp import ClientError, ClientSession

from app.moment import get_current_date
from config import settings
from database import rdbms
from log import LOGGER


async def fetch_algolia_searches(
    session: ClientSession, timeframe: int = 7
) -> Optional[List[dict]]:
    """
    Fetch single week of searches from Algolia API.

    :param ClientSession session: Async HTTP request session.
    :param int timeframe: Number of days for which to fetch recent search analytics.

    :returns: Optional[List[dict]]
    """
    params = {
        "index": "hackers_posts",
        "limit": 999999,
        "startDate": get_current_date(timeframe),
    }
    try:
        async with session.get(
            settings.ALGOLIA_SEARCHES_ENDPOINT, params=params
        ) as resp:
            data = await resp.json()
            return filter_search_queries(data["searches"])
    except ClientError as e:
        LOGGER.error(f"HTTPError while fetching Algolia searches: {e}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching Algolia searches: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching Algolia searches: {e}")


def filter_search_queries(
    search_queries: List[Optional[Dict[str, Any]]]
) -> List[Optional[Dict[str, Any]]]:
    """
    Filter noisy or irrelevant search analytics from results (ie: too short).

    :param List[Optional[Dict[str, Any]]] search_queries: JSON representing search queries submitted by users.

    :returns: List[Optional[Dict[str, Any]]]
    """
    search_queries = [query for query in search_queries if len(query["search"]) > 3]
    return search_queries


async def import_algolia_search_queries(records: List[dict], table_name: str) -> str:
    """
    Save history of search queries executed on the site.

    :param List[dict] records: JSON of search queries submitted by users.
    :param str table_name: Name of SQL table to save data to.

    :returns: str
    """
    rows = await rdbms.insert_records(
        records,
        table_name,
        "analytics",
        replace=True,
    )
    return rows
