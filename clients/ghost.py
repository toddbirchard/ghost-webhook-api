"""Ghost admin."""
from typing import Tuple
from datetime import datetime as date
import requests
from requests.exceptions import RequestException
import jwt
from api.log import LOGGER


class Ghost:
    """Ghost admin client."""

    def __init__(
            self,
            base_url,
            version,
            client_id,
            client_secret
    ):
        """
        Creates a new Ghost API client.

        :param base_url: The base url of the server
        :param version: The server version to use
        :param client_id: Self-supplied client ID
        :param client_secret: Self-supplied client secret
        """
        self.client_id = client_id
        self.secret = client_secret
        self.url = f'{base_url}/ghost/api/v{version}'

    def __https_session(self) -> None:
        """Authorize HTTPS session with Ghost admin."""
        endpoint = f'{self.url}/session/'
        headers = {'Authorization': self.session_token}
        req = requests.post(endpoint, headers=headers)
        LOGGER.info(f'Authorization resulted in status code {req.status_code}.')

    @property
    def session_token(self) -> str:
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

    def get_post(self, post_id) -> dict:
        """Fetch post data by ID."""
        headers = {'Authorization': self.session_token}
        req = requests.get(f"{self.url}/posts/{post_id}", headers=headers)
        return req.json()

    def update_post(self, post_id, body: dict, slug: str) -> Tuple[dict, int]:
        """Update post by ID."""
        try:
            req = requests.put(
                f'{self.url}/posts/{post_id}/',
                json=body,
                headers={'Authorization': self.session_token}
            )
            response = f'Received code {req.status_code} when updating `{slug}`.'
            LOGGER.info(response)
            return {'RESPONSE': response}, req.status_code
        except RequestException as exc:
            LOGGER.error(exc)
            raise exc

    def get_json_backup(self) -> dict:
        """Download JSON snapshot of Ghost database."""
        self.__https_session()
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

