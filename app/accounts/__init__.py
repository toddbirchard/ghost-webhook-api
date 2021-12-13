"""User account management & functionality."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.accounts.subscriptions import new_ghost_subscription
from clients import ghost, mailgun
from database.crud import (
    create_account,
    create_comment,
    create_donation,
    get_account,
    get_comment_upvote,
    get_donation,
    remove_comment_upvote,
    submit_comment_upvote,
)
from database.models import Account, Comment
from database.orm import get_db
from database.schemas import (
    NetlifyAccountCreationResponse,
    NetlifyUserEvent,
    NewComment,
    NewDonation,
    UpvoteComment,
)
from log import LOGGER

router = APIRouter(prefix="/account", tags=["accounts"])


@router.post(
    "/",
    summary="Create new account from Netlify",
    description="Create user account sourced from Netlify Identity.",
    response_model=NetlifyAccountCreationResponse,
)
async def new_account(
    new_account_event: NetlifyUserEvent, db: Session = Depends(get_db)
):
    """
    Create user account from Netlify identity signup.

    :param NetlifyUserEvent new_account_event: Newly created user account from Netlify.
    :param Session db: ORM Database session.

    :returns: NetlifyAccountCreationResponse
    """
    account = new_account_event.user
    db_account = get_account(db, account.email)
    if db_account:
        LOGGER.warning(f"User account already exists for `{account.email}`.")
        raise HTTPException(
            status_code=400,
            detail=f"User account already exists for `{account.email}`.",
        )
    create_account(db, account)
    db_account_created = get_account(db, account.email)
    if db_account_created:
        return NetlifyAccountCreationResponse(
            succeeded=new_account_event,
            failed=None,
        )
    return NetlifyAccountCreationResponse(
        succeeded=None,
        failed=new_account_event,
    )


@router.post(
    "/comment",
    summary="New user comment",
    description="Save user-generated comments submitted on posts.",
    response_model=NewComment,
)
async def new_comment(comment: NewComment, db: Session = Depends(get_db)):
    """
    Save user comment to database and notify post author.

    :param NewComment comment: User-submitted comment.
    :param Session db: ORM Database session.
    """
    LOGGER.info(f"Attempting to create new comment: {comment.__dict__}")
    post = ghost.get_post(comment.post_id)
    if post is None:
        LOGGER.error(f"Failed to create new comment; post_id {comment.post_id} does not exist ({comment.post_slug})")
    authors = ghost.get_authors()
    create_comment(db, comment)
    post_author = f"{comment.author_name} <{comment.author_email}>"
    if comment.user_email not in authors:
        mailgun.email_notification_new_comment(post, [post_author], comment.__dict__)
    ghost.rebuild_netlify_site()
    return comment


@router.post(
    "/comment/upvote",
    summary="Upvote a comment",
    description="Increment a comment's upvote count, or revoke an existing upvote from a user.",
    response_model=UpvoteComment,
)
async def upvote_comment(upvote_request: UpvoteComment, db: Session = Depends(get_db)):
    """
    Cast a user upvote for another user's comment.

    :param UpvoteComment upvote_request: User-generated request to upvote a comment.
    :param Session db: ORM Database session.
    """
    existing_vote = get_comment_upvote(
        db, upvote_request.user_id, upvote_request.comment_id
    )
    if upvote_request.vote and existing_vote is None:
        submit_comment_upvote(db, upvote_request.user_id, upvote_request.comment_id)
        return upvote_request
    elif upvote_request.vote and existing_vote:
        LOGGER.warning(
            f"Upvote already submitted for comment `{upvote_request.comment_id}` from user `{upvote_request.user_id}`."
        )
        raise HTTPException(
            status_code=400,
            detail=f"Upvote already submitted for comment `{upvote_request.comment_id}` from user `{upvote_request.user_id}`.",
        )
    elif upvote_request.vote is False and existing_vote:
        remove_comment_upvote(db, upvote_request.user_id, upvote_request.comment_id)
        return upvote_request
    elif upvote_request.vote is False and existing_vote is None:
        LOGGER.warning(
            f"Can't delete non-existent upvote for comment `{upvote_request.comment_id}` from user `{upvote_request.user_id}`."
        )
        raise HTTPException(
            status_code=400,
            detail=f"Can't delete non-existent upvote for comment `{upvote_request.comment_id}` from user `{upvote_request.user_id}`.",
        )


@router.post(
    "/donation",
    summary="New BuyMeACoffee donation",
    description="Save record of new donation to persistent ledger.",
    response_model=NewDonation,
)
async def accept_donation(donation: NewDonation, db: Session = Depends(get_db)):
    """
    Save BuyMeACoffee donation to database.

    :param NewDonation donation: New donation.
    :param Session db: ORM Database session.
    """
    db_donation = get_donation(db, donation.coffee_id)
    if db_donation:
        LOGGER.warning(
            f"Donation `{donation.coffee_id}` from `{donation.email}` already exists."
        )
        raise HTTPException(
            status_code=400,
            detail=f"Donation `{donation.coffee_id}` from `{donation.email}` already exists.",
        )
    create_donation(db=db, donation=donation)
    ghost.rebuild_netlify_site()
    return donation


@router.get("/comments", summary="Test get comments via ORM")
async def test_orm(db: Session = Depends(get_db)):
    """Test endpoint for fetching comments joined with user info."""
    comments = db.query(Comment).join(Account, Comment.user_id == Account.id).all()
    for comment in comments:
        LOGGER.info(comment.user)
    return comments
