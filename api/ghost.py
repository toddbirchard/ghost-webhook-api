"""Ghost admin."""
from datetime import datetime as date
import requests
from requests.exceptions import RequestException
import jwt
from api.log import LOGGER


class Ghost:
    """Ghost admin client."""

    def __init__(self, api_key, url):
        self.api_key = api_key
        self.client_id = api_key.split(':')[0]
        self.secret = api_key.split(':')[1]
        self.url = url
        self.token = None

    def _https_session(self):
        """Authorize HTTPS session with Ghost admin."""
        endpoint = f'{self.url}/session/'
        headers = {'Authorization': self.session_token}
        req = requests.post(endpoint, headers=headers)
        LOGGER.info(f'Authorization resulted in status code {req.status_code}.')

    @property
    def session_token(self):
        """Generate session token for Ghost admin API."""
        iat = int(date.now().timestamp())
        header = {
            'alg': 'HS256',
            'typ': 'JWT',
            'kid': self.client_id
        }
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,
            'aud': '/v3/admin/'
        }
        token = jwt.encode(
            payload,
            bytes.fromhex(self.secret),
            algorithm='HS256',
            headers=header
        )
        return f'Ghost {token.decode()}'

    def get_post(self, post_id):
        """Fetch post data by ID."""
        headers = {'Authorization': self.session_token}
        req = requests.get(f"{self.url}/posts/{post_id}", headers=headers)
        return req.json()

    def update_post(self, post_id, body):
        """Update post by ID."""
        title = body['posts'][0]
        try:
            req = requests.put(
                f'{self.url}/posts/{post_id}/',
                json=body,
                headers={'Authorization': self.session_token}
            )
            return {post_id: f'Received code {req.status_code} when updating `{title}`.'}
        except RequestException as exc:
            LOGGER.error(exc)
            raise exc

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
