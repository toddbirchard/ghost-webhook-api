"""Ghost admin client."""
from datetime import datetime as date
import requests
import jwt
from api.log import logger


class Ghost:

    def __init__(self, api_key):
        self.api_key = api_key
        self.id = api_key.split(':')[0]
        self.secret = api_key.split(':')[1]

    @staticmethod
    def _https_session(url, key):
        """Authorize HTTPS session with Ghost admin."""
        token = f'Ghost {key}'
        endpoint = f'{url}/ghost/api/v3/admin/session/'
        headers = {'Origin': 'hackersandslackers.tools', 'Authorization': token}
        r = requests.post(endpoint, headers=headers)
        logger.info(f'Authorization resulted in status code {r.status_code}.')

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

    def get_json_backup(self, url, key):
        """Attempt to extract JSON snapshot of Ghost database."""
        self._https_session(url, key)
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;\
                                q=0.9,image/webp,image/apng,*/*;\
                                q=0.8,application/signed-exchange;\
                                v=b3;q=0.9',
                   'accept-encoding': 'gzip, deflate, br',
                   'Origin': 'hackersandslackers.tools',
                   'Authority': 'hackersandslackers.tools'}
        endpoint = f'{url}/ghost/api/v3/admin/db/'
        r = requests.get(endpoint, headers=headers)
        return r.json()
