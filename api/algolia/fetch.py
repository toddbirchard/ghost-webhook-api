"""Fetch data from Algolia REST API."""
import requests
from flask import current_app as api


def weekly_searches():
    """Fetch single week of analytics from Algolia API."""
    endpoint = f'{api.config["ALGOLIA_BASE_URL"]}/searches'
    headers = {'x-algolia-application-id': api.config["ALGOLIA_APP_ID"],
               'x-algolia-api-key': api.config["ALGOLIA_API_KEY"]}
    params = {'index': 'hackers_posts',
              'limit': 999999}
    r = requests.get(endpoint, headers=headers, params=params)
    return r.json()['searches']
