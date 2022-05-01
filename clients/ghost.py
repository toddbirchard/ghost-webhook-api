"""Ghost admin client."""
from datetime import datetime as date
from typing import List, Optional, Tuple

import jwt
import requests
from requests.exceptions import HTTPError

from log import LOGGER


class Ghost:
    """Ghost admin client."""

    def __init__(
        self,
        admin_api_url: str,
        content_api_url: str,
        client_id: str,
        client_secret: str,
        netlify_build_url: str,
        content_api_key: str,
    ):
        """
        Ghost Admin API client constructor.

        :param str client_id: Self-supplied client ID
        :param str client_secret: Self-supplied client secret
        :param str admin_api_url: Ghost's admin API base URL
        :param str netlify_build_url: Netlify webhook to trigger full site rebuild.
        """
        self.client_id = client_id
        self.content_api_url = content_api_url
        self.secret = client_secret
        self.admin_api_url = admin_api_url
        self.netlify_build_url = netlify_build_url
        self.content_api_key = content_api_key

    def _https_session(self) -> None:
        """Authorize HTTPS session with Ghost admin."""
        endpoint = f"{self.admin_api_url}/session/"
        headers = {"Authorization": self.session_token}
        resp = requests.post(endpoint, headers=headers)
        LOGGER.info(f"Authorization resulted in status code {resp.status_code}.")

    @property
    def session_token(self) -> str:
        """Generate session token for Ghost admin API."""
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": self.client_id}
        payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/v3/admin/"}
        token = jwt.encode(
            payload, bytes.fromhex(self.secret), algorithm="HS256", headers=header
        )
        return token

    def get_post(self, post_id: str) -> Optional[dict]:
        """
        Fetch Ghost post by ID.

        :param str post_id: ID of post to fetch.

        :returns: Optional[dict]
        """
        try:
            headers = {
                "Authorization": f"Ghost {self.session_token}",
                "Content-Type": "application/json",
            }
            params = {
                "include": "authors",
                "formats": "mobiledoc,html",
            }
            endpoint = f"{self.admin_api_url}/posts/{post_id}/"
            resp = requests.get(endpoint, headers=headers, params=params)
            if resp.json().get("errors") is not None:
                LOGGER.error(
                    f"Failed to fetch post `{post_id}`: {resp.json().get('errors')[0]['message']}"
                )
                return None
            elif resp.json().get("posts"):
                post = resp.json()["posts"][0]
                LOGGER.info(f"Fetched Ghost post `{post['slug']}` ({endpoint})")
                return post
            return None
        except HTTPError as e:
            LOGGER.error(f"Ghost HTTPError while fetching post `{post_id}`: {e}")
        except KeyError as e:
            LOGGER.error(f"KeyError for `{e}` occurred while fetching post `{post_id}`")
        except Exception as e:
            LOGGER.error(
                f"Unexpected error occurred while fetching post `{post_id}`: {e}"
            )

    def get_post_by_slug(self, post_slug: str) -> Optional[dict]:
        """
        Fetch Ghost post by slug.

        :param str post_slug: Unique slug of post to fetch.

        :returns: Optional[dict]
        """
        try:
            headers = {
                "Authorization": f"Ghost {self.session_token}",
                "Content-Type": "application/json",
            }
            params = {
                "include": "authors",
                "formats": "mobiledoc",
            }
            endpoint = f"{self.admin_api_url}/posts/slug/{post_slug}/"
            resp = requests.get(endpoint, headers=headers, params=params)
            if resp.json().get("errors") is not None:
                LOGGER.error(
                    f"Failed to fetch post `{post_slug}`: {resp.json().get('errors')[0]['message']}"
                )
                return None
            post = resp.json()["posts"][0]
            LOGGER.info(f"Fetched Ghost post `{post['slug']}` ({endpoint})")
            return post
        except HTTPError as e:
            LOGGER.error(f"Ghost HTTPError while fetching post `{post_slug}`: {e}")
        except KeyError as e:
            LOGGER.error(
                f"KeyError for `{e}` occurred while fetching post `{post_slug}`"
            )
        except Exception as e:
            LOGGER.error(
                f"Unexpected error occurred while fetching post `{post_slug}`: {e}"
            )

    def get_pages(self) -> Optional[dict]:
        """
        Fetch Ghost pages.

        :returns: Optional[dict]
        """
        try:
            headers = {
                "Authorization": f"Ghost {self.session_token}",
                "Content-Type": "application/json",
            }
            endpoint = f"{self.admin_api_url}/pages"
            resp = requests.get(endpoint, headers=headers)
            if resp.json().get("errors") is not None:
                LOGGER.error(
                    f"Failed to fetch Ghost pages: {resp.json().get('errors')[0]['message']}"
                )
                return None
            post = resp.json()["pages"]
            LOGGER.info(f"Fetched Ghost pages` ({endpoint})")
            return post
        except HTTPError as e:
            LOGGER.error(f"Ghost HTTPError while fetching pages: {e}")
        except KeyError as e:
            LOGGER.error(f"KeyError for `{e}` occurred while fetching pages")
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred while fetching pages: {e}")

    def update_post(self, post_id: str, body: dict, slug: str) -> Tuple[str, int]:
        """
        Update post by ID.

        :param str post_id: Ghost post ID
        :param dict body: Payload containing post updates.
        :param str slug: Human-readable unique identifier.

        :returns: Tuple[str, int]
        """
        try:
            resp = requests.put(
                f"{self.admin_api_url}/posts/{post_id}/",
                json=body,
                headers={
                    "Authorization": self.session_token,
                    "Content-Type": "application/json",
                },
            )
            if resp.status_code > 300:
                LOGGER.warning(f"Failed to update post `{slug}`: {resp.text}")
            LOGGER.success(f"Successfully updated post `{slug}`: {body}")
            return resp.status_code
        except HTTPError as e:
            LOGGER.error(e.response)
            return e.response.content, e.response.status_code

    def get_all_authors(self) -> Optional[List[dict]]:
        """
        Fetch all Ghost authors.

        :returns: Optional[List[dict]]
        """
        try:
            params = {"key": self.content_api_key}
            headers = {
                "Authorization": f"Ghost {self.session_token}",
                "Content-Type": "application/json",
            }
            resp = requests.get(
                f"{self.admin_api_url}/users", params=params, headers=headers
            )
            if resp.status_code == 200:
                return resp.json().get("users")
        except HTTPError as e:
            LOGGER.error(f"Failed to fetch Ghost authors: {e.response.content}")
        except KeyError as e:
            LOGGER.error(f"KeyError while fetching Ghost authors: {e}")

    def get_author(self, author_id: int) -> Optional[List[str]]:
        """
        Fetch single Ghost author.

        :param int author_id: ID of Ghost author to fetch.

        :returns: Optional[List[str]]
        """
        try:
            params = {"key": self.content_api_key}
            headers = {
                "Content-Type": "application/json",
            }
            resp = requests.get(
                f"{self.content_api_url}/authors/{author_id}/",
                params=params,
                headers=headers,
            )
            if resp.status_code == 200:
                return resp.json()["authors"]
        except HTTPError as e:
            LOGGER.error(
                f"Failed to fetch Ghost authorID={author_id}: {e.response.content}"
            )
        except KeyError as e:
            LOGGER.error(f"KeyError while fetching Ghost authorID={author_id}: {e}")

    def create_member(self, body: dict) -> Tuple[str, int]:
        """
        Create new Ghost member account used to receive newsletters.

        :param dict body: Payload containing member information.

        :returns: Optional[List[str]]
        """
        try:
            resp = requests.post(
                f"{self.admin_api_url}/members/",
                json=body,
                headers={"Authorization": self.session_token},
            )
            response = f'Successfully created new Ghost member `{body.get("email")}: {resp.json()}.'
            LOGGER.success(response)
            return response, resp.status_code
        except HTTPError as e:
            LOGGER.error(f"Failed to create Ghost member: {e.response.content}")
            return e.response.content, e.response.status_code

    def rebuild_netlify_site(self) -> Tuple[str, int]:
        """
        Trigger Netlify site rebuild.

        :returns: Tuple[str, int]
        """
        try:
            resp = requests.post(
                self.netlify_build_url,
            )
            LOGGER.info(f"Triggered Netlify build with status code {resp.status_code}.")
            return (
                f"Triggered Netlify build with status code {resp.status_code}.",
                resp.status_code,
            )
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
        endpoint = f"{self.admin_api_url}/db/"
        try:
            resp = requests.get(endpoint, headers=headers)
            return resp.json()
        except HTTPError as e:
            LOGGER.error(e.response)
            return e.response

    def get_all_posts(self):
        try:
            headers = {
                "Authorization": f"Ghost {self.session_token}",
                "Content-Type": "application/json",
            }
            params = {
                "limit": "200",
            }
            endpoint = f"{self.admin_api_url}/posts"
            resp = requests.get(endpoint, headers=headers, params=params)
            if resp.json().get("errors") is not None:
                LOGGER.error(
                    f"Failed to fetch posts: {resp.json().get('errors')[0]['message']}"
                )
                return None
            posts = resp.json()["posts"]
            return [
                post["url"].replace(".app", ".com")
                for post in posts
                if post["status"] == "published"
            ]
        except HTTPError as e:
            LOGGER.error(f"Ghost HTTPError while fetching posts: {e}")
        except KeyError as e:
            LOGGER.error(f"KeyError for `{e}` occurred while fetching posts")
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred while fetching posts: {e}")
