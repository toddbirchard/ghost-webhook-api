"""Manage Ghost Newsletter subscriptions."""

from fastapi import APIRouter, HTTPException

from app.newsletter.newsletter import welcome_newsletter_subscriber
from database.schemas import GhostMember, GhostSubscriber
from log import LOGGER

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post(
    "/",
    summary="Add new user account to Ghost.",
    description="Create free-tier Ghost membership for Netlify user account upon signup.",
    response_model=GhostSubscriber,
)
async def new_ghost_member(subscriber: GhostSubscriber) -> GhostSubscriber:
    """
    Welcome new Ghost subscriber & add analytics.

    :param GhostSubscriber subscriber: Ghost newsletter subscriber with updated info.

    :returns: GhostSubscriber
    """
    try:
        current_member = subscriber.current
        welcome_newsletter_subscriber(current_member)
        return subscriber
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected exception when sending `welcome` email: {e}",
        )


@router.delete(
    "/",
    summary="Delete Ghost Member.",
    description="Unsubscribe existing Ghost member from newsletters.",
    response_model=GhostMember,
)
async def member_unsubscribe(subscriber: GhostSubscriber):
    """
    Log user unsubscribe events.

    :param GhostSubscriber subscriber: Current Ghost newsletter subscriber.
    """
    subscriber = subscriber.previous
    LOGGER.info(f"`{subscriber.name}` unsubscribed from newsletter.")
