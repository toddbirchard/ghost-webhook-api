"""Create Twilio SMS client."""
from twilio.rest import Client


class Twilio:

    def __init__(self, Config):
        self.sid = Config.TWILIO_ACCOUNT_SID
        self.token = Config.TWILIO_AUTH_TOKEN
        self.recipient = Config.TWILIO_RECIPIENT_PHONE
        self.sender = Config.TWILIO_SENDER_PHONE
        self.client = Client(self.sid, self.token)

    def send_message(self, msg):
        """Send Twilio message."""
        message = self.client.messages.create(
            to=self.recipient,
            from_=self.sender,
            body=msg
        )
        return message
