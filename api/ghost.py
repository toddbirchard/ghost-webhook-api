"""Ghost admin client."""
from datetime import datetime as date
import requests
import jwt
from api.log import LOGGER


class Ghost:
    """Ghost admin client."""

    def __init__(self, api_key, url):
        self.api_key = api_key
        self.id = api_key.split(':')[0]
        self.secret = api_key.split(':')[1]
        self.url = url
        self.token = None

    def _https_session(self):
        """Authorize HTTPS session with Ghost admin."""
        token = f'Ghost {self.get_session_token()}'
        endpoint = f'{self.url}/session/'
        headers = {'Authorization': token}
        req = requests.post(endpoint, headers=headers)
        LOGGER.info(f'Authorization resulted in status code {req.status_code}.')

    def get_session_token(self):
        """Generate token for Ghost admin API."""
        iat = int(date.now().timestamp())
        header = {
            'alg': 'HS256',
            'typ': 'JWT',
            'kid': self.id
        }
        payload = {'iat': iat,
                   'exp': iat + 5 * 60,
                   'aud': '/v3/admin/'}
        token = jwt.encode(
            payload,
            bytes.fromhex(self.secret),
            algorithm='HS256',
            headers=header
        )
        return f'Ghost {token.decode()}'

    def get_post(self, post_id):
        """Fetch post JSON by ID."""
        token = self.get_session_token()
        headers = {'Authorization': token}
        req = requests.get(f"{self.url}/posts/{post_id}", headers=headers)
        return req.json()

    def update_post(self, post_id, body):
        """Update post."""
        token = self.get_session_token()
        headers = {'Authorization': token}
        req = requests.put(f"{self.url}/posts/{post_id}", json=body, headers=headers)
        return req.json()

    def get_json_backup(self):
        """Attempt to extract JSON snapshot of Ghost database."""
        self._https_session()
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;\
                                q=0.9,image/webp,image/apng,*/*;\
                                q=0.8,application/signed-exchange;\
                                v=b3;q=0.9',
                   'accept-encoding': 'gzip, deflate, br',
                   'Origin': 'hackersandslackers.tools',
                   'Authority': 'hackersandslackers.tools'}
        endpoint = f'{self.url}/db/'
        req = requests.get(endpoint, headers=headers)
        return req.json()
