"""Create Mailgun client."""
from typing import Optional

import requests
from requests import HTTPError, request

from clients.log import LOGGER


class Mailgun:
    """Mailgun email Client."""

    def __init__(self, server: str, from_address: str, api_key: str):
        self.server = server
        self.from_address = from_address
        self.api_key = api_key
        self.endpoint = f"https://api.mailgun.net/v3/{self.server}/messages"

    def send_email(self, body: dict) -> Optional[request]:
        """Send Mailgun email."""
        try:
            req = requests.post(
                self.endpoint,
                auth=("api", self.api_key),
                data=body,
            )
            LOGGER.success(
                f"Successfully sent email to {body['to']} with subject `{body['subject']}`"
            )
            return req
        except HTTPError as e:
            LOGGER.error(
                f"Failed to send email to `{body['to']}` with subject `{body['subject']}`: {e}"
            )
            return None

    def send_comment_notification_email(
        self, post: dict, comment: dict
    ) -> Optional[request]:
        """Notify post author when a comment is submitted."""
        body = {
            "from": "todd@hackersandslackers.com",
            "to": post["primary_author"]["email"],
            "subject": f"Hackers and Slackers: {comment.get('user_name')} commented on your post `{post['title']}`",
            "o:tracking": True,
            "text": f"Your post `{post['title']}` received a comment. {comment.get('user_name')} says: \n\n{comment.get('body')} \n\nSee the comment here: {post['url'].replace('.app', '.com')}",
        }
        return self.send_email(body)
