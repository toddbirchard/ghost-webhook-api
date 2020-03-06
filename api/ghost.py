"""Ghost admin client."""
from datetime import datetime as date
import jwt


class Ghost:

    def __init__(self, api_key):
        self.api_key = api_key
        self.id = api_key.split(':')[0]
        self.secret = api_key.split(':')[1]

    def get_session_token(self):
        """Generate token for Ghost admin API."""
        iat = int(date.now().timestamp())
        headers = {'alg': 'HS256', 'typ': 'JWT', 'kid': self.id}
        payload = {'iat': iat,
                   'exp': iat + 5 * 60,
                   'aud': '/v3/admin/'}
        token = jwt.encode(payload,
                           bytes.fromhex(self.secret),
                           algorithm='HS256',
                           headers=headers)
        return token
