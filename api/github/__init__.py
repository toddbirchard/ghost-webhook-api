"""Notify upon Github activity."""
from flask import current_app as api
from flask import make_response, request
from api import sms
from api.log import LOGGER


@LOGGER.catch
@api.route('/github/notifications', methods=['POST'])
def update_post():
    """Send SMS notification upon Github activity by users."""
    payload = request.get_json()
    action = payload['action']
    user = payload['sender'].get('login')
    if user == 'toddbirchard':
        return make_response('Activity ignored.', 200)
    sms.send_message(payload)
    return make_response('SMS notification sent.', 200)



