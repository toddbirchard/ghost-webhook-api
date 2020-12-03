"""Newsletter subscription management."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.newsletter.models import Subscription
from clients import mailgun
from clients.log import LOGGER
from config import Settings

router = APIRouter(prefix="/subscription", tags=["newsletter"])


@router.post("/")
async def newsletter_subscribe(subscription: Subscription):
    """Send welcome email to newsletter subscriber."""
    body = {
        "from": "todd@hackersandslackers.com",
        "to": subscription.member.current.email,
        "subject": Settings().MAILGUN_SUBJECT_LINE,
        "template": Settings().MAILGUN_EMAIL_TEMPLATE,
        "h:X-Mailgun-Variables": {"name": subscription.member.current.name},
        "o:tracking": True,
    }
    response = mailgun.send_email(body)
    return {subscription.member.current.email: f"{response.status_code}"}


@router.delete("/")
def newsletter_unsubscribe(subscription: Subscription):
    """Track user unsubscribe events and spam complaints."""
    LOGGER.info(f"{subscription.member.previous.name} unsubscribed from newsletter.")
    return subscription.member.previous
