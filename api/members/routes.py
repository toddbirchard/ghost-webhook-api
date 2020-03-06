from flask import current_app as api
from mixpanel import Mixpanel
from flask import make_response, request, jsonify


@api.route('/members/mixpanel', methods=['POST'])
def subscriber_mixpanel():
    mp = Mixpanel(api.config['mixpanel_api_token'])
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    if email:
        body = {'$name': name, '$email': email}
        mp.people_set(email, body)
        return make_response(jsonify({'CREATED': body}))
    return make_response(jsonify({'DENIED': body}))
