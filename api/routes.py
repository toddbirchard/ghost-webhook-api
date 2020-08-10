"""API health check."""
from flask import current_app as api
from flask import make_response
from api.log import LOGGER


@LOGGER.catch
@api.route('/', methods=['GET'])
def health_check():
    """API health check status."""
    headers = {'Content-Type': 'text/plain;charset=utf-8'}
    return make_response('API is online!', 200, headers)
