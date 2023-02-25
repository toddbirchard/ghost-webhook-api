"""Fetch site traffic & search query analytics."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.analytics.algolia import persist_algolia_searches
from app.analytics.plausible import fetch_top_visited_posts
from config import settings
from database.schemas import AnalyticsRowsUpdated
from log import LOGGER

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/",
    summary="Import site analytics.",
    description="Import site performance analytics from a data warehouse to a SQL database.",
    response_model=AnalyticsRowsUpdated,
    status_code=200,
)
async def migrate_site_analytics() -> AnalyticsRowsUpdated:
    """
    Fetch top searches for weekly & monthly time frames.

    :returns: AnalyticsRowsUpdated
    """
    week_num_hits, week_pages_visited = fetch_top_visited_posts("7d", limit=100)
    month_num_hits, month_pages_visited = fetch_top_visited_posts("month", limit=500)
    LOGGER.success(f"Inserted {week_num_hits} rows into `weekly_stats`, {month_num_hits}  into `monthly_stats`.")
    return AnalyticsRowsUpdated(
        week={"total": week_num_hits, "rows": week_pages_visited},
        month={"total": month_num_hits, "rows": month_pages_visited},
    )


@router.get(
    "/searches/",
    summary="Import user search queries.",
    description="Store user search queries to a SQL database for analysis and suggestive search.",
    status_code=200,
)
async def save_user_search_queries() -> JSONResponse:
    """
    Save top search analytics for the current week.

    :returns: JSONResponse
    """
    weekly_searches = persist_algolia_searches(settings.ALGOLIA_TABLE_WEEKLY, 7)
    monthly_searches = persist_algolia_searches(settings.ALGOLIA_TABLE_MONTHLY, 90)
    if weekly_searches is None or monthly_searches is None:
        HTTPException(500, "Unexpected error when saving search query data.")
    LOGGER.success(
        f"Inserted {len(weekly_searches)} rows into `{settings.ALGOLIA_TABLE_WEEKLY}`, \
            {len(monthly_searches)} into `{settings.ALGOLIA_TABLE_MONTHLY}`"
    )
    return JSONResponse(
        {
            "7-Day": {
                "count": len(weekly_searches),
                "rows": weekly_searches,
            },
            "90-Day": {
                "count": len(monthly_searches),
                "rows": monthly_searches,
            },
        }
    )
