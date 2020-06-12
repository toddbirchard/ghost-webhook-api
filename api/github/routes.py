"""Routes to receive Github webhooks."""
import requests
from flask import current_app as api
from flask import jsonify, make_response, request
from api.log import LOGGER


@LOGGER.catch
@api.route('/github/issue', methods=['POST'])
def maintenance_queries():
    """Send notification upon Github issue creation."""
    issue = request.get_json()
    endpoint = f'https://api.mailgun.net/v3/{api.config["MAILGUN_EMAIL_SERVER"]}/messages'
    body = {
        "from": "todd@mail.hackersandslackers.com",
        "to": api.config["MAILGUN_PERSONAL_EMAIL"],
        "subject": 'New Github issue created.',
        "text": issue
    }
    req = requests.post(
        endpoint,
        auth=("api", api.config["MAILGUN_API_KEY"]),
        data=body,
    )
    return make_response(jsonify(issue), 200)
