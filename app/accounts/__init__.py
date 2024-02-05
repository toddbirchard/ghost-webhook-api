"""User account management & functionality."""

from fastapi import APIRouter, HTTPException

from config import settings
from database import ghost_db
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
    try:
        sql_query = ""
        with open(f"{settings.BASE_DIR}/database/queries/posts/selects/get_comments.sql", "r", encoding="utf-8") as f:
            sql_query = f.read()
        comments = ghost_db.execute_query(sql_query)
        comments = [dict(r._mapping) for r in comments]
        LOGGER.success(f"Successfully fetched {len(comments)} Ghost comments.")
        return comments
    except HTTPException as e:
        LOGGER.error(f"HTTPException while fetching Ghost comments: {e}")
        return {"errors": f"Failed to fetch Ghost comments: {e}"}
