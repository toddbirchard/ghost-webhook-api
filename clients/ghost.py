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
        api_version: int,
        content_api_url: str,
        content_api_key: str,
        client_id: str,
        client_secret: str,
    ):
        """
        Ghost Admin API client constructor.

        :param str admin_api_url: Admin URL of self-hosted Ghost API.
        :param int content_api_url: Content URL of self-hosted Ghost API.
        :param str api_version: Version of Ghost API.
        :param str content_api_key: Content API key for self-hosted Ghost API.
        :param str client_id: Unique ID of Ghost admin client.
        :param str client_secret: Authentication secret of Ghost admin client.
        """
        self.admin_api_url = admin_api_url
        self.api_version = api_version
        self.client_id = client_id
        self.content_api_url = content_api_url
        self.secret = client_secret
        self.content_api_key = content_api_key

    def _https_session(self) -> None:
        """Authorize HTTPS session with Ghost admin."""
        endpoint = f"{self.admin_api_url}/session/"
        headers = {"Authorization": self.session_token}
        resp = requests.post(endpoint, headers=headers, timeout=20)
        LOGGER.info(f"Authorization resulted in status code {resp.status_code}.")

    @property
    def session_token(self) -> str:
        """Generate session token for Ghost admin API."""
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": self.client_id}
        payload = {"iat": iat, "exp": iat + 5 * 60, "aud": f"/v{self.api_version}/admin/"}
        token = jwt.encode(payload, bytes.fromhex(self.secret), algorithm="HS256", headers=header)
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
            resp = requests.get(endpoint, headers=headers, params=params, timeout=20)
            if resp.json().get("errors") is not None and resp.json().get("posts") is not None:
                LOGGER.error(f"Failed to fetch post `{post_id}`: {resp.json().get('errors')[0]['message']}")
            post = resp.json()["posts"][0]
            LOGGER.info(f"Fetched Ghost post `{post['slug']}` ({endpoint})")
            return post
        except HTTPError as e:
            LOGGER.error(f"Ghost HTTPError while fetching post `{post_id}`: {e}")
        except KeyError as e:
            LOGGER.error(f"KeyError for `{e}` occurred while fetching post `{post_id}`")
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred while fetching post `{post_id}`: {e}")

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
            resp = requests.get(endpoint, headers=headers, params=params, timeout=20)
            post = resp.json()["posts"][0]
            LOGGER.info(f"Fetched Ghost post `{post['slug']}`")
            return post
        except HTTPError as e:
            LOGGER.error(f"HTTPError occurred while fetching post `{post_slug}`: {e}")
        except LookupError as e:
            LOGGER.warning(f"LookupError occurred while fetching post `{post_slug}`: `{e}`")
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred while fetching post `{post_slug}`: {e}")

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
            resp = requests.get(endpoint, headers=headers, timeout=20)
            if resp.json().get("errors") is not None:
                LOGGER.error(f"Failed to fetch Ghost pages: {resp.json().get('errors')[0]['message']}")
            LOGGER.info(f"Fetched {len(resp.json())} Ghost pages")
            return resp.json().get("pages")
        except HTTPError as e:
            LOGGER.error(f"Ghost HTTPError while fetching pages: {e}")
        except KeyError as e:
            LOGGER.error(f"KeyError for `{e}` occurred while fetching pages")
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred while fetching pages: {e}")

    def update_post(self, post_id: str, body: dict, slug: str) -> Optional[dict]:
        """
        Update post by ID.

        :param str post_id: Ghost post ID
        :param dict body: Payload containing post updates.
        :param str slug: Human-readable unique identifier.

        :returns: Optional[dict]
        """
        try:
            resp = requests.put(
                f"{self.admin_api_url}/posts/{post_id}/",
                json=body,
                headers={
                    "Authorization": self.session_token,
                    "Content-Type": "application/json",
                },
                timeout=20,
            )
            if resp.status_code != 200:
                LOGGER.success(f"Successfully updated post `{slug}`")
                return resp.json()
        except HTTPError as e:
            LOGGER.error(f"HTTPError while updating Ghost post: {e}")
        except Exception as e:
            LOGGER.error(f"Unexpected error while updating Ghost post: {e}")

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
            resp = requests.get(f"{self.admin_api_url}/users", params=params, headers=headers, timeout=20)
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
                timeout=20,
            )
            if resp.status_code == 200:
                return resp.json()["authors"]
        except HTTPError as e:
            LOGGER.error(f"Failed to fetch Ghost authorID={author_id}: {e.response.content}")
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
                timeout=20,
            )
            response = f'Successfully created new Ghost member `{body.get("email")}: {resp.json()}.'
            LOGGER.success(response)
            return response, resp.status_code
        except HTTPError as e:
            LOGGER.error(f"Failed to create Ghost member: {e.response.content}")
            return e.response.content, e.response.status_code

    def get_all_posts(self) -> Optional[List[str]]:
        """
        Fetch all Ghost post URLs.

        :returns: Optional[List[str]]
        """
        try:
            headers = {
                "Authorization": f"Ghost {self.session_token}",
                "Content-Type": "application/json",
            }
            params = {
                "filter": "type:post",
            }
            endpoint = f"{self.admin_api_url}/posts"
            resp = requests.get(endpoint, headers=headers, params=params, timeout=20)
            if resp.status_code == 200:
                posts = resp.json()["posts"]
                return [post["url"] for post in posts if post["status"] == "published"]
        except HTTPError as e:
            LOGGER.error(f"Ghost HTTPError while fetching posts: {e}")
        except KeyError as e:
            LOGGER.error(f"KeyError for `{e}` occurred while fetching posts")
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred while fetching posts: {e}")
