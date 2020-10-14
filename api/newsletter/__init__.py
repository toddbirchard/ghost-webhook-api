"""Newsletter subscription management."""
from flask import current_app as api
from flask import make_response, request, jsonify
import simplejson as json
import requests
from clients.log import LOGGER


@api.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    """Send welcome email to newsletter subscriber."""
    endpoint = f'https://api.mailgun.net/v3/{api.config["MAILGUN_EMAIL_SERVER"]}/messages'
    email = request.json.get('email')
    name = request.json.get('name').title()
    body = {
        "from": "todd@mail.hackersandslackers.com",
        "to": email,
        "subject": api.config["MAILGUN_SUBJECT_LINE"],
        "template": api.config["MAILGUN_EMAIL_TEMPLATE"],
        "h:X-Mailgun-Variables": json.dumps({"name": name})
    }
    req = requests.post(
        endpoint,
        auth=("api", api.config["MAILGUN_API_KEY"]),
        data=body,
    )
    LOGGER.info(f'Welcome email sent to {name} <{email}>.')
    return make_response(jsonify(req.json()), 200, {'Content-Type': 'application/json'})


@api.route('/newsletter/unsubscribe', methods=['POST'])
def newsletter_unsubscribe():
    """Track user unsubscribe events and spam complaints."""
    data = request.get_json()
    LOGGER.warning(data)
    return make_response(jsonify(data), 200, {'Content-Type': 'application/json'})
