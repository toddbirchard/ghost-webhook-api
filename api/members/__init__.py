"""Ghost member management."""
from datetime import datetime
import simplejson as json
from flask import current_app as api
from flask import make_response, request, jsonify
import requests
from mixpanel import Mixpanel
from clients import db, ghost
from clients.log import LOGGER


@api.route('/members/signup', methods=['POST'])
def new_user():
    """Create Ghost member from Netlify identity signup."""
    data = request.get_json()
    body = {
      "members": [{
        "name": data.get('name'),
        "email": data.get('email'),
        "note": data.get('ip_address'),
        "subscribed": True,
        "comped": False,
        "labels": [data.get('provider')]
      }]
    }
    response, code = ghost.create_member(body)
    LOGGER.infop(response)
    return make_response(response, code)


@LOGGER.catch
@api.route('/members/comments', methods=['POST'])
def new_comment():
    """Parse form submission into comment SQL table."""
    data = request.get_json()
    LOGGER.info(data)
    user_role = data.get('user_role', None)
    if data.get('author_name') == data.get('user_name'):
        user_role = 'author'
    comment = {
        "comment_id": data.get('id'),
        "user_name": data.get('user_name'),
        "user_avatar": data.get('user_avatar'),
        "user_id": data.get('user_id'),
        "body": data.get('body'),
        "post_id": data.get('post_id'),
        "post_slug": data.get('post_slug'),
        "user_role": user_role,
        "created_at": datetime.strptime(
            data.get('created_at').replace('Z', ''),
            "%Y-%m-%dT%H:%M:%S.%f"
        ),
    }
    result = db.insert_records(
        [comment],
        table_name="comments",
        database_name="hackers_prod"
    )
    LOGGER.info(f'Created commentId={comment["comment_id"]} by user={comment["user_id"]}.')
    return make_response(jsonify(result), 200)


@api.route('/members/mixpanel', methods=['POST'])
def subscriber_mixpanel():
    """Create Mixpanel record for newsletter subscriber."""
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


@api.route('/members/newsletter', methods=['POST'])
def newsletter_subscriber():
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


@api.route('/members/donation', methods=['PUT'])
def donation_received():
    """Add donation to historical ledger."""
    donation = request.get_json()
    email = donation.get('email')
    name = donation.get('email')
    link = donation.get('link')
    created_at = donation.get('created_at')
    count = donation.get('count')
    coffee_id = donation.get('coffee_id')
    message = donation.get('message')
    if message:
        message = message.replace("'", "\\'")
    donation_data = {
        "email": email,
        "name": name,
        "link": link,
        "created_at": created_at,
        "count": count,
        "coffee_id": coffee_id,
        "message": message
    }
    existing_donation = db.fetch_record(
        f"SELECT * FROM donations WHERE email = '{email}';",
        database_name='analytics',
    )
    if existing_donation and email:
        db.execute_query(f"DELETE FROM donations WHERE email = {email}")
    db.insert_records(
        [donation_data],
        table_name="donations",
        database_name="analytics"
    )
    LOGGER.info(f'Received donation: {donation}')
    return make_response(
        jsonify({'Inserted': donation}),
        200,
        {'content-type': 'application/json'}
    )
