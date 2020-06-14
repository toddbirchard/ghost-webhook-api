"""Fetch posts from Algolia REST API."""
import requests
from flask import current_app as api


def fetch_weekly_searches():
    """Fetch single week of searches from Algolia API."""
    endpoint = f'{api.config["ALGOLIA_BASE_URL"]}/searches'
    headers = {
        'x-algolia-application-id': api.config["ALGOLIA_APP_ID"],
        'x-algolia-api-key': api.config["ALGOLIA_API_KEY"]
    }
    params = {'index': 'hackers_posts', 'limit': 999999}
    req = requests.get(endpoint, headers=headers, params=params)
    return req.json()['searches']
