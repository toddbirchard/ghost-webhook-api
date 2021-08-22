from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi_mail.email_utils import DefaultChecker

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
async def new_ghost_member(subscriber: Subscriber) -> JSONResponse:
    """
    Welcome new Ghost subscriber & add analytics.

    :param Subscriber subscriber: New subscriber to Hackers newsletter.

    :returns: JSONResponse
    """
    try:
        subscriber = subscriber.current
        email = newsletter_subscribe(subscriber)
        return JSONResponse({"email": email})
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


async def default_checker():
    checker = (
        DefaultChecker()
    )  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains()  # require to fetch temporary email domains
    return checker


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
