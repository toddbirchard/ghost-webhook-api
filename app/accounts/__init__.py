"""User account management & functionality."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import settings
from database import ghost_db
from database.crud import get_account
from database.orm import get_db
from log import LOGGER

router = APIRouter(prefix="/account", tags=["accounts"])


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
    sql_query = ""
    with open(f"{settings.BASE_DIR}/database/queries/comments/get_comments.sql", "r", encoding="utf-8") as f:
        sql_query = f.read()
    comments = ghost_db.execute_query(sql_query).fetchall()
    comments = [dict(r._mapping) for r in comments]
    LOGGER.success(f"Successfully fetched {len(comments)} Ghost comments.")
    return comments
