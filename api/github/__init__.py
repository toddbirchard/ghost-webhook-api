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
    action = payload.get('action')
    user = payload['sender'].get('login')
    if user == 'toddbirchard':
        return make_response('Activity ignored.', 200, {'content-type': 'text/html; charset=UTF-8'})
    sms.send_message(payload)
    return make_response(f'SMS notification sent for {action} for {user}.', 200, {'content-type': 'text/html; charset=UTF-8'})



