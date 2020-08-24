"""Create Twilio SMS client."""
from twilio.rest import Client


class Twilio:
    """Twilio SMS Client."""

    def __init__(self, sid: str, token: str, recipient: str, sender: str):
        self.sid = sid
        self.token = token
        self.recipient = recipient
        self.sender = sender
        self.client = Client(self.sid, self.token)

    def send_message(self, msg):
        """Send Twilio message."""
        message = self.client.messages.create(
            to=self.recipient,
            from_=self.sender,
            body=msg
        )
        return message
