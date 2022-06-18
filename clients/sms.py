"""Create Twilio SMS client."""
from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance

from log import LOGGER


class Twilio:
    """Twilio SMS Client."""

    def __init__(self, sid: str, token: str, recipient: str, sender: str):
        self.sid = sid
        self.token = token
        self.recipient = recipient
        self.sender = sender
        self.client = Client(self.sid, self.token)

    def send_message(self, message_body: str) -> MessageInstance:
        """
        Send Twilio message.

        :param str message_body: Content of SMS message to send.

        :returns: MessageInstance
        """
        LOGGER.info(f"SMS triggered by post edit: {message_body}")
        sms_message = self.client.messages.create(
            to=self.recipient, from_=self.sender, body=message_body
        )
        return sms_message
