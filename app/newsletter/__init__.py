"""Manage Ghost Newsletter subscriptions."""
from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi_mail.email_utils import DefaultChecker

from app.newsletter.mixpanel import create_mixpanel_record
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

    :param Subscriber subscriber: Current Ghost newsletter subscriber.
    """
    subscriber = subscriber.previous
    LOGGER.info(f"`{subscriber.name}` unsubscribed from newsletter.")


async def default_checker() -> Type[DefaultChecker]:
    """
    Return email validator to ensure incoming email is legitimate.

    :returns: DefaultChecker
    """
    checker = DefaultChecker()  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains()  # require to fetch temporary email domains
    return DefaultChecker


@router.get("/email/disposable")
async def simple_send(domain: str = Query(...), checker: DefaultChecker = Depends(default_checker)) -> JSONResponse:
    """
    Check that email recipient is legit.

    :param str domain: TLD of email address.
    :param DefaultChecker checker: Email validator.

    :returns: JSONResponse
    """
    if await checker.is_dispasoble(domain):
        return JSONResponse(status_code=400, content={"message": "this is disposable domain"})
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
