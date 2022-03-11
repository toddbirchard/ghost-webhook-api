"""Manage Ghost Newsletter subscriptions."""
from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi_mail.email_utils import DefaultChecker

from app.newsletter.member import parse_ghost_member_json
from app.newsletter.mixpanel import create_mixpanel_record
from app.newsletter.newsletter import welcome_newsletter_subscriber
from database.schemas import Member, Subscriber
from log import LOGGER

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post(
    "/",
    summary="Add new user account to Ghost.",
    description="Create free-tier Ghost membership for Netlify user account upon signup.",
)
async def new_ghost_member(subscriber: Subscriber) -> JSONResponse:
    """
    Welcome new Ghost subscriber & add analytics.

    :param Subscriber subscriber: New subscriber to Hackers newsletter.

    :returns: JSONResponse
    """
    try:
        current_member = subscriber.current
        welcome_email = welcome_newsletter_subscriber(current_member)
        member_json = parse_ghost_member_json(current_member)
        member_json.update({"welcome_email": welcome_email})
        previous_member = subscriber.previous
        if previous_member is not None:
            previous_member_json = parse_ghost_member_json(current_member)
            member_json.update({"previous": previous_member_json})
        return JSONResponse(member_json)
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
    LOGGER.info(f"`{subscriber.name}` unsubscribed from newsletter.")


async def default_checker() -> Type[DefaultChecker]:
    """
    Return email validator to ensure incoming email is legitimate.

    :returns: DefaultChecker
    """
    checker = (
        DefaultChecker()
    )  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains()  # require to fetch temporary email domains
    return DefaultChecker


@router.get("/email/disposable")
async def simple_send(
    domain: str = Query(...), checker: DefaultChecker = Depends(default_checker)
) -> JSONResponse:
    """
    Check that email recipient is legit.

    :param str domain: TLD of email address.
    :param DefaultChecker checker: Email validator.

    :returns: JSONResponse
    """
    if await checker.is_dispasoble(domain):
        return JSONResponse(
            status_code=400, content={"message": "this is disposable domain"}
        )
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
