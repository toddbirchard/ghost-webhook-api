from flask import current_app as api
from flask import make_response, request, jsonify


@api.route('/', methods=['GET'])
def cpanel():
    """Panel UI for triggering endpoints."""
    pass
