"""Fetch site traffic & search query analytics."""
from fastapi import APIRouter

from app.analytics.plausible import top_visited_pages_by_timeframe
from database.schemas import AnalyticsResponse
from log import LOGGER

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/",
    summary="Import site analytics.",
    description="Import site performance analytics from a data warehouse to a SQL database.",
    response_model=AnalyticsResponse,
    status_code=200,
)
async def migrate_site_analytics():
    """Fetch top searches for weekly & monthly time periods."""
    weekly_traffic = top_visited_pages_by_timeframe("7d", limit=100)
    monthly_traffic = top_visited_pages_by_timeframe("30d", limit=500)
    LOGGER.success(
        f"Inserted {len(weekly_traffic)} rows into `weekly_stats`,  {len(monthly_traffic)}  into `monthly_stats`."
    )
    return {
        "weekly_stats": {
            "count": len(weekly_traffic),
            "rows": weekly_traffic,
        },
        "monthly_stats": {
            "count": len(monthly_traffic),
            "rows": monthly_traffic,
        },
    }


'''@router.get(
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
    weekly_searches = persist_algolia_searches(settings.ALGOLIA_TABLE_WEEKLY, "7d")
    monthly_searches = persist_algolia_searches(settings.ALGOLIA_TABLE_MONTHLY, "month")
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
    )'''
