"""Fetch top search queries."""
from flask import current_app as api
from flask import jsonify, make_response
from api import db
from api.log import LOGGER
from .fetch import fetch_weekly_searches


@LOGGER.catch
@api.route('/searches/week', methods=['GET'])
def week_searches():
    """Save top Algolia searches for the current week."""
    records = fetch_weekly_searches()
    response = db.insert_records(records, 'algolia_searches_week', replace=True)
    LOGGER.info(response)
    return make_response(jsonify(response), 200)


@LOGGER.catch
@api.route('/searches/historical', methods=['GET'])
def historical_searches():
    """Save and persist top Algolia searches for the current month."""
    records = fetch_weekly_searches()
    response = db.insert_records(records, 'algolia_searches_historical')
    LOGGER.info(response)
    return make_response(jsonify(response), 200)
