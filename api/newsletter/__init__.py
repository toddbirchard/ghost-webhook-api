"""Newsletter subscription management."""
import simplejson as json
from flask import current_app as api
from flask import jsonify, make_response, request

from clients import mailgun
from clients.log import LOGGER


@api.route("/newsletter/subscribe", methods=["POST"])
def newsletter_subscribe():
    """Send welcome email to newsletter subscriber."""
    email = request.json.get("email")
    name = request.json.get("name").title()
    body = {
        "from": "todd@hackersandslackers.com",
        "to": email,
        "subject": api.config["MAILGUN_SUBJECT_LINE"],
        "template": api.config["MAILGUN_EMAIL_TEMPLATE"],
        "h:X-Mailgun-Variables": json.dumps({"name": name}),
        "o:tracking": True,
    }
    response = mailgun.send_email(body)
    if response.status_code == 200:
        return make_response(response.json(), 200, {"Content-Type": "application/json"})
    return make_response(response, 202, {"Content-Type": "text/plain"})


@api.route("/newsletter/unsubscribe", methods=["POST"])
def newsletter_unsubscribe():
    """Track user unsubscribe events and spam complaints."""
    data = request.get_json()
    LOGGER.warning(data)
    return make_response(jsonify(data), 200, {"Content-Type": "application/json"})
