from fastapi import APIRouter, HTTPException
from mixpanel import MixpanelException

from app.members.mixpanel import create_mixpanel_record
from app.members.newsletter import newsletter_subscribe
from database.schemas import Member, Subscriber
from log import LOGGER

router = APIRouter(prefix="/members", tags=["members"])


@router.post(
    "/",
    summary="Add new user account to Ghost.",
    description="Create free-tier Ghost membership for Netlify user account upon signup.",
)
async def new_ghost_member(user_event: Subscriber):
    """
    Welcome new Ghost subscriber & add analytics.

    :param user_event: Newly created user account.
    :type user_event: Subscriber
    """
    try:
        user = user_event.current
        email = newsletter_subscribe(user)
        mx = create_mixpanel_record(user)
        return {"email": email, "mixpanel": mx}
    except MixpanelException as e:
        LOGGER.error(f"Error creating user in Mixpanel: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error creating user in Mixpanel: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected exception when adding Ghost member: {e}",
        )


@router.delete(
    "/",
    summary="Delete Ghost Member.",
    description="Unsubscribe existing Ghost member from newsletters.",
    response_model=Member,
)
async def member_unsubscribe(subscription: Subscriber):
    """Track user unsubscribe events and spam complaints."""
    subscriber = subscription.previous
    LOGGER.info(f"`{subscriber.name}` unsubscribed from members.")
    return subscription
