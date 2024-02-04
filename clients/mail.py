"""Create Mailgun client."""

from typing import List

import requests
from requests import HTTPError, Response

from log import LOGGER


class Mailgun:
    """Mailgun email client."""

    def __init__(self, mail_server: str, from_address: str, api_key: str):
        self.mail_server = mail_server
        self.from_address = from_address
        self.api_key = api_key
        self.endpoint = f"https://api.mailgun.net/v3/{self.mail_server}/messages"

    def send_email(self, body: dict, test_mode=False) -> Response:
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
            LOGGER.error(f"HTTPError error while sending email to `{body['to']}` subject `{body['subject']}`: {e}")
        except Exception as e:
            LOGGER.error(f"Unexpected error while sending email to `{body['to']}` subject `{body['subject']}`: {e}")

    def email_notification_new_comment(self, post: dict, recipient: List[str], comment: dict, test_mode=False) -> dict:
        """
        Notify author when a user comments on a post.

        :param dict post: Ghost post body fetched from admin API.
        :param List[str] recipient: Email recipient.
        :param dict comment: User comment on a post.
        :param bool test_mode: Flag to indicate email is being sent for test purposes.

        :returns: dict
        """
        body = {
            "from": "Todd Birchard <postmaster@mail.hackersandslackers.com>",
            "to": recipient,
            "subject": f"Hackers and Slackers: {comment.get('user_name')} commented on your post `{post['title']}`",
            "o:tracking": True,
            "o:tracking-opens": True,
            "o:tracking-clicks": True,
            "text": f"Your post `{post['title']}` received a comment. {comment.get('user_name')} says: \n\n{comment.get('body')} \n\nSee the comment here: {post['url'].replace('.app', '.com')}",
        }
        email_response = self.send_email(body, test_mode)
        if email_response.status_code == 200:
            LOGGER.success(f"Successfully send comment notification to {recipient}: {body}")
            return {
                "status": {
                    "sent": True,
                    "code": email_response.status_code,
                    "error": None,
                },
                "email": body,
            }
        else:
            LOGGER.error(
                f"Failed to send comment notification to {recipient} with error {email_response.status_code} ({email_response.json()}): {body}"
            )
            return {
                "status": {
                    "sent": False,
                    "code": email_response.status_code,
                    "error": email_response.json(),
                },
                "email": body,
            }
