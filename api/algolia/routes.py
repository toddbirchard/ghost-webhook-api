from flask import current_app as api
from flask import jsonify, make_response
from api import db
from api.log import logger
from .fetch import fetch_weekly_searches


@logger.catch
@api.route('/searches/week', methods=['GET'])
def week_searches():
    """Save top Algolia searches for the current week."""
    records = fetch_weekly_searches()
    upload = db.insert_records(records, 'algolia_searches_week', replace=True)
    return make_response(jsonify(upload), 200)


@logger.catch
@api.route('/searches/historical', methods=['GET'])
def historical_searches():
    """Save Algolia searches to persistent database."""
    records = fetch_weekly_searches()
    upload = db.insert_records(records, 'algolia_searches_historical')
    return make_response(jsonify(upload), 200)
