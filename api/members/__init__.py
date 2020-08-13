"""Subscribers and Ghost member management."""
import simplejson as json
from flask import current_app as api
from flask import make_response, request, jsonify
import requests
from mixpanel import Mixpanel
from clients import db
from clients.log import LOGGER


@LOGGER.catch
@api.route('/members/mixpanel', methods=['POST'])
def subscriber_mixpanel():
    """Create Mixpanel record for new subscriber."""
    mp = Mixpanel(api.config['MIXPANEL_API_TOKEN'])
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    if email:
        body = {'$name': name, '$email': email}
        mp.people_set(email, body)
        LOGGER.info(f'Created Mixpanel record for subscriber {name}, ({email}).')
        return make_response(jsonify({'CREATED': body}))
    return make_response(jsonify({'DENIED': data}))


@LOGGER.catch
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
    req = requests.post(
        endpoint,
        auth=("api", api.config["MAILGUN_API_KEY"]),
        data=body,
    )
    LOGGER.info(f'Welcome email successfully sent to {name} <{email}>.')
    return make_response(jsonify(req.json()), 200)


@LOGGER.catch
@api.route('/members/donation', methods=['POST'])
def donation_received():
    """Parse incoming donations."""
    donation = request.get_json()
    email = donation.get('email')
    name = donation.get('name')
    message = donation.get('message')
    link = donation.get('link')
    coffee_id = donation.get('coffee_id')
    existing_donation = db.fetch_record(
        f"SELECT * FROM donations WHERE email = '{email}';",
        table_name='donations'
    )
    if existing_donation:
        db.update(f"UPDATE donations SET message = '{message}', link = '{link}', name = '{name}', coffee_id = '{coffee_id}' WHERE email = '{email}';")
    results = db.insert_records(donation, 'coffee', replace=False)
    LOGGER.info(results)
    return make_response(jsonify(results))
