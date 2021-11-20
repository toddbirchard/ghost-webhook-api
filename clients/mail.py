"""Create Mailgun client."""
from typing import Optional

import requests
from fastapi_mail.email_utils import DefaultChecker
from requests import HTTPError, Response

from config import settings
from log import LOGGER


class Mailgun:
    """Mailgun email Client."""

    def __init__(self, mail_server: str, from_address: str, api_key: str):
        self.mail_server = mail_server
        self.from_address = from_address
        self.api_key = api_key
        self.endpoint = f"https://api.mailgun.net/v3/{self.mail_server}/messages"

    def send_email(self, body: dict, test_mode=False) -> Optional[Response]:
        """
        Send email via Mailgun.

        :param dict body: Properties of outbound email.
        :param bool test_mode: Flag to indicate email is being sent for test purposes.

        :returns: Optional[Response]
        """
        try:
            if test_mode is True:
                body.update({"o:testmode": True})
            return requests.post(
                self.endpoint,
                auth=("api", self.api_key),
                data=body,
            )
        except HTTPError as e:
            LOGGER.error(
                f"HTTPError error while sending email to `{body['to']}` subject `{body['subject']}`: {e}"
            )
        except Exception as e:
            LOGGER.error(
                f"Unexpected error while sending email to `{body['to']}` subject `{body['subject']}`: {e}"
            )

    def email_notification_new_comment(
        self, post: dict, comment: dict, test_mode=False
    ) -> Optional[Response]:
        """
        Notify author when a user comments on a post.

        :param dict post: Ghost post body fetched from admin API.
        :param dict comment: User comment on a post.
        :param bool test_mode: Flag to indicate email is being sent for test purposes.

        :returns: Optional[Response]
        """
        body = {
            "from": "Todd Birchard <postmaster@mail.hackersandslackers.com>",
            "to": post["primary_author"]["email"],
            "subject": f"Hackers and Slackers: {comment.get('user_name')} commented on your post `{post['title']}`",
            "o:tracking": True,
            "o:tracking-opens": True,
            "o:tracking-clicks": True,
            "text": f"Your post `{post['title']}` received a comment. {comment.get('user_name')} says: \n\n{comment.get('body')} \n\nSee the comment here: {post['url'].replace('.app', '.com')}",
        }
        return self.send_email(body, test_mode)


async def default_checker():
    checker = (
        DefaultChecker()
    )  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains()  # require to fetch temporary email domains
    return checker
