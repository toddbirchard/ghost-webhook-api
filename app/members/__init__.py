from fastapi import APIRouter, HTTPException
from mixpanel import MixpanelException

from app.members.mixpanel import create_mixpanel_record
from app.members.newsletter import newsletter_subscribe
from clients.log import LOGGER
from database.schemas import Member, Subscriber

router = APIRouter(prefix="/member", tags=["members"])


@router.post(
    "/",
    summary="Add new user account to Ghost.",
    description="Create free-tier Ghost membership for Netlify user account upon signup.",
)
async def new_ghost_member(user_event: Subscriber):
    """
    Create Ghost member.

    :param user_event: Newly created user account.
    :type user_event: GhostMemberEvent
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
    description="Create free-tier Ghost membership for Netlify user account upon signup.",
)
async def newsletter_unsubscribe(member: Member):
    """Track user unsubscribe events and spam complaints."""
    LOGGER.info(f"`{member.name}` unsubscribed from newsletter.")
    return member.dict()
