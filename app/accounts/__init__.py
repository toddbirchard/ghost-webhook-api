"""User account management & functionality."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import ghost_db
from database.crud import create_account, get_account
from database.orm import get_db
from database.schemas import NetlifyAccountCreationResponse, NetlifyUserEvent
from config import BASE_DIR
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


@router.get(
    "/comments/",
    summary="Get all user comments.",
    description="Fetch all user-created comments on Ghost posts.",
)
async def get_comments():
    """
    Fetch all user-created comments on Ghost posts.

    :returns: List[Comment]
    """
    comments = ghost_db.execute_query_from_file(
        f"{BASE_DIR}/database/queries/comments/selects/get_comments.sql"
    ).fetchall()
    LOGGER.success(f"Successfully fetched {len(comments)} Ghost comments.")
    return comments
