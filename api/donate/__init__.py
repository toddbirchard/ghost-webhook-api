"""Donations received from BuyMeACoffee."""
from flask import current_app as api
from flask import jsonify, make_response, request
from api import db
from api.log import LOGGER


@LOGGER.catch
@api.route('/donate', methods=['POST'])
def donation_received():
    """Parse incoming donations."""
    donation = request.get_json()
    results = db.insert_records(donation, 'coffee', replace=False)
    LOGGER.info(results)
    return make_response(jsonify(results))
