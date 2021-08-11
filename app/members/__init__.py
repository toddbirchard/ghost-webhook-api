from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from mixpanel import MixpanelException

from app.members.mixpanel import create_mixpanel_record
from app.members.newsletter import newsletter_subscribe
from database.schemas import Member, Subscriber
from log import LOGGER

router = APIRouter(prefix="/members", tags=["members"])


@router.post(
    "/welcome",
    summary="Add new user account to Ghost.",
    description="Create free-tier Ghost membership for Netlify user account upon signup.",
)
async def new_ghost_member(subscriber: Subscriber):
    """
    Welcome new Ghost subscriber & add analytics.

    :param Subscriber subscriber: New subscriber to Hackers newsletter.
    """
    try:
        subscriber = subscriber.current
        email = newsletter_subscribe(subscriber)
        return JSONResponse({"email": email})
    except MixpanelException as e:
        LOGGER.error(f"Error creating user in Mixpanel: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error creating user in Mixpanel: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected exception when sending `welcome` email: {e}",
        )


@router.delete(
    "/",
    summary="Delete Ghost Member.",
    description="Unsubscribe existing Ghost member from newsletters.",
    response_model=Member,
)
async def member_unsubscribe(subscriber: Subscriber):
    """
    Log user unsubscribe events.

    :param Subscriber subscriber: Current Ghost newsletter subscriber.
    """
    subscriber = subscriber.previous
    LOGGER.info(f"`{subscriber.name}` unsubscribed from members.")
