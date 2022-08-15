"""Welcome newsletter subscribers ."""
from typing import Optional

from clients import mailgun
from config import settings
from database.schemas import GhostMember, SubscriptionWelcomeEmail
from log import LOGGER


def welcome_newsletter_subscriber(
    subscriber: GhostMember,
) -> Optional[SubscriptionWelcomeEmail]:
    """
    Send welcome email to newsletter subscriber.

    :param Member subscriber: New Ghost member with newsletter subscription.

    :returns: Optional[SubscriptionWelcomeEmail]
    """
    body = {
        "from": settings.MAILGUN_FROM_SENDER,
        "to": [subscriber.email],
        "subject": settings.MAILGUN_SUBJECT_LINE,
        "template": settings.MAILGUN_NEWSLETTER_TEMPLATE,
        "h:X-Mailgun-Variables": {"name": subscriber.name},
        "o:tracking": True,
    }
    response = mailgun.send_email(body)
    if response.status_code != 200:
        LOGGER.error(f"Mailgun failed to send welcome email: {body}")
        return None
    return SubscriptionWelcomeEmail(
        from_email=settings.MAILGUN_PERSONAL_EMAIL,
        to_email=subscriber.email,
        subject=settings.MAILGUN_SUBJECT_LINE,
        template=settings.MAILGUN_NEWSLETTER_TEMPLATE,
    )
