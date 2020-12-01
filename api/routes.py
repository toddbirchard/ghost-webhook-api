"""API health check."""
from flask import current_app as api
from flask import jsonify, make_response

from clients.log import LOGGER


@api.route("/", methods=["GET"])
def health_check():
    """API health check status."""
    urls = [
        f"{rule.rule} {rule.methods}"
        for rule in api.url_map.iter_rules()
        if "GET" in rule.methods or "POST" in rule.methods
    ]
    headers = {"Content-Type": "application/json"}
    LOGGER.success("API health check successful")
    return make_response(jsonify(urls), 200, headers)
