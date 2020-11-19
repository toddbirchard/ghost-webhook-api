"""Ghost admin client."""
from datetime import datetime as date
from typing import Tuple, Optional

import jwt
import requests
from requests.exceptions import HTTPError

from clients.log import LOGGER


class Ghost:
    """Ghost admin client."""

    def __init__(
        self, api_url: str, client_id: str, client_secret: str, netlify_build_url: str
    ):
        """
        Ghost admin API client constructor.

        :param client_id: Self-supplied client ID
        :param client_secret: Self-supplied client secret
        :param api_url: Ghost's admin API base URL
        :param netlify_build_url: Netlify hook to trigger full site rebuild.
        """
        self.client_id = client_id
        self.secret = client_secret
        self.url = api_url
        self.netlify_build_url = netlify_build_url

    def _https_session(self) -> None:
        """Authorize HTTPS session with Ghost admin."""
        endpoint = f"{self.url}/session/"
        headers = {"Authorization": self.session_token}
        req = requests.post(endpoint, headers=headers)
        LOGGER.info(f"Authorization resulted in status code {req.status_code}.")

    @property
    def session_token(self) -> str:
        """Generate session token for Ghost admin API."""
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": self.client_id}
        payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/v3/admin/"}
        token = jwt.encode(
            payload, bytes.fromhex(self.secret), algorithm="HS256", headers=header
        )
        LOGGER.info(f"Granted Ghost auth token.")
        return f"Ghost {token.decode()}"

    def get_post(self, post_id) -> Optional[dict]:
        """Fetch post by ID."""
        try:
            headers = {"Authorization": self.session_token}
            params = {"include": "authors"}
            req = requests.get(
                f"{self.url}/posts/{post_id}", headers=headers, params=params
            )
            return req.json()
        except HTTPError as e:
            LOGGER.error(f"Failed to fetch post `{post_id}`: {e}")

    def update_post(self, post_id: str, body: dict, slug: str) -> Tuple[str, int]:
        """
        Update post by ID.

        :param post_id: Ghost post ID
        :type post_id: str
        :param body: Payload containing post updates.
        :type body: dict
        :param slug: Human-readable post identifier.
        :type slug: str
        """
        try:
            req = requests.put(
                f"{self.url}/posts/{post_id}/",
                json=body,
                headers={
                    "Authorization": self.session_token,
                    "Content-Type": "application/json",
                },
            )
            response = f"Received code {req.status_code} when updating `{slug}`."
            if req.status_code > 300:
                LOGGER.warning(f"Failed to update post `{slug}`: {req.text}")
            else:
                LOGGER.info(f"Successfully updated post `{slug}`: {body}")
            return response, req.status_code
        except HTTPError as e:
            LOGGER.error(e.response)
            return e.response.content, e.response.status_code

    def create_member(self, body: dict) -> Tuple[str, int]:
        """Create new member.

        :param body: Create new Ghost member account used to receive newsletters.
        :param body: dict
        """
        try:
            req = requests.post(
                f"{self.url}/members/",
                json=body,
                headers={"Authorization": self.session_token},
            )
            response = f'Successfully created new Ghost member `{body.get("email")}: {req.json()}.'
            LOGGER.success(response)
            return response, req.status_code
        except HTTPError as e:
            LOGGER.error(f"Failed to create Ghost member: {e.response.content}")
            return e.response.content, e.response.status_code

    def rebuild_netlify_site(self) -> Tuple[str, int]:
        """Trigger Netlify site rebuild."""
        try:
            req = requests.post(
                self.netlify_build_url,
            )
            response = f"Triggered Netlify build with status code {req.status_code}."
            LOGGER.info(response)
            return response, req.status_code
        except HTTPError as e:
            LOGGER.error(f"Failed to rebuild Netlify site: {e.response.content}")
            return e.response.content, e.response.status_code

    def get_json_backup(self) -> dict:
        """Download JSON snapshot of Ghost database."""
        self._https_session()
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;\
                                q=0.9,image/webp,image/apng,*/*;\
                                q=0.8,application/signed-exchange;\
                                v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "Origin": "hackersandslackers.tools",
            "Authority": "hackersandslackers.tools",
        }
        endpoint = f"{self.url}/db/"
        try:
            req = requests.get(endpoint, headers=headers)
            return req.json()
        except HTTPError as e:
            LOGGER.error(e.response)
            return e.response
