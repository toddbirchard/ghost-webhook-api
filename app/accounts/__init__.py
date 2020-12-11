"""User account functionality."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.accounts.comments import parse_comment
from app.accounts.mixpanel import create_mixpanel_record
from database.schemas import NewComment, NewDonation, UserEvent
from app.accounts.subscriptions import new_ghost_subscription
from clients import ghost, mailgun
from clients.log import LOGGER
from database.crud import create_comment, create_donation, get_comment, get_donation
from database.orm import get_db

router = APIRouter(prefix="/account", tags=["accounts"])


@router.post("/")
def new_ghost_member(user_event: UserEvent):
    """
    Create Ghost member from Netlify identity signup.

    :param user_event: Newly created user account.
    :type user_event: UserEvent
    """
    user = user_event.member.current
    response, code = new_ghost_subscription(user)
    mx = create_mixpanel_record(user)
    return {"ghost": response, "mixpanel": mx}


@router.post(
    "/comment",
    summary="New user comment",
    description="Store user-generated comments submitted on posts.",
)
def new_comment(comment: NewComment, db: Session = Depends(get_db)):
    """
    Save user-generated comment to SQL table, and notify post author.

    :param comment: User-submitted comment.
    :type comment: NewComment
    :param db: ORM Database session.
    :type db: Session
    """
    post = ghost.get_post(comment.post_id)
    authors = ghost.get_authors()
    if comment.user_email not in authors:
        mailgun.send_comment_notification_email(post, comment.__dict__)
    existing_comment = get_comment(db, comment.comment_id)
    if existing_comment:
        raise HTTPException(status_code=400, detail="Comment already created")
    result = create_comment(db, comment)
    LOGGER.success(
        f"New comment `{comment.comment_id}` saved on post `{comment.post_slug}`"
    )
    ghost.rebuild_netlify_site()
    return result.__dict__


@router.post(
    "/donation",
    response_model=NewDonation,
    summary="New BuyMeACoffee donation",
    description="Save record of new donation to persistent ledger.",
)
def accept_donation(donation: NewDonation, db: Session = Depends(get_db)):
    """
    Save donations from BuyMeACoffee to database.

    :param donation: New donation.
    :type donation: NewDonation
    :param db: ORM Database session.
    :type db: Session
    """
    db_user = get_donation(db, donation.coffee_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Donation already created")
    result = create_donation(db=db, donation=donation)
    if bool(result):
        return donation
