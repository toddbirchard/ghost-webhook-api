from flask import current_app as api
from flask import jsonify, make_response
from api import db
from .fetch import weekly_searches


@api.route('/searches', methods=['GET'])
def top_searches():
    """Fetch top searches for the current week."""
    records = weekly_searches()
    upload = db.insert_records(records)
    return make_response(jsonify(upload), 200)