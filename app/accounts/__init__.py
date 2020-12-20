"""User account functionality."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.accounts.mixpanel import create_mixpanel_record
from app.accounts.subscriptions import new_ghost_subscription
from clients import ghost, mailgun
from database.crud import create_comment, create_donation, get_donation
from database.orm import get_db
from database.schemas import NewComment, NewDonation, UserEvent

router = APIRouter(prefix="/account", tags=["accounts"])


@router.post(
    "/",
    summary="Add new user account to Ghost.",
    description="Create free-tier Ghost membership for Netlify user account upon signup.",
)
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
    response_model=NewComment,
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
    user_comment = create_comment(db, comment)
    ghost.rebuild_netlify_site()
    return NewComment.parse_obj(user_comment.dict())


@router.post(
    "/donation",
    summary="New BuyMeACoffee donation",
    description="Save record of new donation to persistent ledger.",
    response_model=NewDonation,
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
    return create_donation(db=db, donation=donation)
