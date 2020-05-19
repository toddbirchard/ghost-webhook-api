from flask import current_app as api
from flask import make_response, request, jsonify
from mixpanel import Mixpanel
import requests
import json
from api.log import logger


@logger.catch
@api.route('/members/mixpanel', methods=['POST'])
def subscriber_mixpanel():
    """Create Mixpanel record for new subscriber."""
    mp = Mixpanel(api.config['mixpanel_api_token'])
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    if email:
        body = {'$name': name, '$email': email}
        mp.people_set(email, body)
        logger.info(f'Created Mixpanel record for subscriber {name}, ({email}).')
        return make_response(jsonify({'CREATED': body}))
    return make_response(jsonify({'DENIED': data}))


@logger.catch
@api.route('/members/newsletter/welcome', methods=['POST'])
def newsletter_welcome_message():
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
    r = requests.post(
        endpoint,
        auth=("api", api.config["MAILGUN_API_KEY"]),
        data=body,
    )
    return make_response(jsonify(r.json()), 200)


