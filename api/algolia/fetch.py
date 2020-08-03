"""Fetch posts from Algolia REST API."""
import requests
from flask import current_app as api
from api.moment import get_current_time_algolia


def fetch_algolia_searches(timeframe=7) -> list:
    """Fetch single week of searches from Algolia API."""
    endpoint = f'{api.config["ALGOLIA_BASE_URL"]}/searches'
    headers = {
        'x-algolia-application-id': api.config["ALGOLIA_APP_ID"],
        'x-algolia-api-key': api.config["ALGOLIA_API_KEY"]
    }
    params = {
        'index': 'hackers_posts',
        'limit': 999999,
        'startDate': get_current_time_algolia(timeframe)
    }
    req = requests.get(endpoint, headers=headers, params=params)
    results = req.json()['searches']
    # Filter garbage search results
    results = list(filter(lambda x: len(x['search']) > 2, results))
    results = list(filter(lambda x: x['search'].replace(' ', '') != '', results))
    return results

