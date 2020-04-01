from flask import current_app as api
from flask import jsonify, make_response
from api import db
from .fetch import fetch_weekly_searches


@api.route('/searches/week', methods=['GET'])
def week_searches():
    """Save top Algolia searches for the current week."""
    records = weekly_searches()
    upload = db.insert_records(records, 'algolia_searches_week', replace=True)
    return make_response(jsonify(upload), 200)


@api.route('/searches/historical', methods=['GET'])
def historical_searches():
    """Horde historical Algolia searches."""
    records = weekly_searches()
    upload = db.insert_records(records, 'algolia_searches_historical')
    return make_response(jsonify(upload), 200)
