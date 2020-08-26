"""Fetch posts from Algolia REST API."""
from typing import List
import requests
from flask import current_app as api
from api.moment import get_current_date


def fetch_algolia_searches(timeframe=7) -> List[str]:
    """Fetch single week of searches from Algolia API."""
    endpoint = f'{api.config["ALGOLIA_BASE_URL"]}/searches'
    headers = {
        'x-algolia-application-id': api.config["ALGOLIA_APP_ID"],
        'x-algolia-api-key': api.config["ALGOLIA_API_KEY"]
    }
    params = {
        'index': 'hackers_posts',
        'limit': 999999,
        'startDate': get_current_date(timeframe)
    }
    req = requests.get(endpoint, headers=headers, params=params)
    search_queries = req.json()['searches']
    return filter_results(search_queries)


def filter_results(search_queries: list) -> list:
    """Filter garbage search queries."""
    search_queries = list(filter(lambda x: len(x['search']) > 2, search_queries))
    search_queries = list(filter(lambda x: x['search'].replace(' ', '') != '', search_queries))
    return search_queries
