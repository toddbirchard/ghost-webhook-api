"""Fetch top search queries."""
from flask import current_app as api
from flask import jsonify, make_response
from clients import db
from clients.log import LOGGER
from .fetch import fetch_algolia_searches


@LOGGER.catch
@api.route('/searches/week', methods=['GET'])
def week_searches():
    """Save top search queries for the current week."""
    records = fetch_algolia_searches(timeframe=7)
    response = db.insert_records(
        records,
        table_name='algolia_searches_week',
        database_name='analytics'
        replace=True
    )
    return make_response(jsonify(response), 200)


@LOGGER.catch
@api.route('/searches/historical', methods=['GET'])
def historical_searches():
    """Save and persist top search queries for the current month."""
    records = fetch_algolia_searches(timeframe=30)
    response = db.insert_records(
        records,
        table_name='algolia_searches_historical',
        database_name='analytics'
    )
    return make_response(jsonify(response), 200)
