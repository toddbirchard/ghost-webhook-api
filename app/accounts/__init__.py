"""User account management & functionality."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.accounts.comments import get_user_role
from app.accounts.subscriptions import new_ghost_subscription
from clients import ghost, mailgun
from database.crud import (
    create_account,
    create_comment,
    get_account,
    get_comment_upvote,
    remove_comment_upvote,
    submit_comment_upvote,
)
from database.models import Account, Comment
from database.orm import get_db
from database.schemas import NetlifyAccountCreationResponse, NetlifyUserEvent, NewComment, UpvoteComment
from log import LOGGER

router = APIRouter(prefix="/account", tags=["accounts"])


@router.post(
    "/",
    summary="Create new account from Netlify",
    description="Create user account sourced from Netlify Identity.",
    response_model=NetlifyAccountCreationResponse,
)
async def new_account(new_account_event: NetlifyUserEvent, db: Session = Depends(get_db)):
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
        LOGGER.success(
            f"Account created: id={account.id} email={account.email}, name={account.user_metadata.full_name}"
        )
        return NetlifyAccountCreationResponse(
            succeeded=new_account_event,
            failed=None,
        )
    LOGGER.warning(
        f"Account not created: id={account.id} email={account.email}, name={account.user_metadata.full_name}"
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
    post = ghost.get_post(comment.post_id)
    post_author = f"{post['primary_author']['name']} <{post['primary_author']['email']}>"
    user_role = get_user_role(comment, post)
    if comment.user_email != post["primary_author"]["email"]:
        mailgun.email_notification_new_comment(post, [post_author], comment.__dict__)
    created_comment = create_comment(db, comment, user_role)
    if created_comment:
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
    existing_vote = get_comment_upvote(db, upvote_request.user_id, upvote_request.comment_id)
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
    LOGGER.warning(
        f"Can't delete non-existent upvote for comment `{upvote_request.comment_id}` from user `{upvote_request.user_id}`."
    )
    raise HTTPException(
        status_code=400,
        detail=f"Can't delete non-existent upvote for comment `{upvote_request.comment_id}` from user `{upvote_request.user_id}`.",
    )


@router.get("/comments", summary="Test get comments via ORM")
async def test_orm(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Test endpoint for fetching comments joined with user info.

    :param Session db: ORM Database session.

    :returns: JSONResponse
    """
    all_comments = db.query(Comment).join(Account, Comment.user_id == Account.id).all()
    for comment in all_comments:
        LOGGER.info(comment.user)
    return JSONResponse(all_comments)
