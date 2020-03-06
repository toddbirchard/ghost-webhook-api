from flask import current_app as api
from datetime import datetime as date
import jwt
from api import logger


@logger.catch
def get_session_token():
    """Generate token for Ghost admin API."""
    id, secret = api.config['GHOST_API_KEY'].split(':')
    iat = int(date.now().timestamp())
    headers = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
    payload = {'iat': iat,
               'exp': iat + 5 * 60,
               'aud': '/v3/admin/'}
    token = jwt.encode(payload,
                       bytes.fromhex(secret),
                       algorithm='HS256',
                       headers=headers)
    return token
