"""Enrich tag metadata."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database import rdbms
from database.read_sql import collect_sql_queries
from log import LOGGER

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get(
    "/",
    summary="Optimize tag metadata.",
    description="Performs multiple actions to optimize tag SEO.",
)
async def update_tags_metadata() -> JSONResponse:
    """
    Enrich tag metadata upon update.

    :returns: JSONResponse
    """
    tag_update_queries = collect_sql_queries("tags")
    update_results = rdbms.execute_queries(tag_update_queries, "hackers_dev")
    LOGGER.success(f"Updated tags metadata: {update_results}")
    return JSONResponse(update_results, status_code=200)
