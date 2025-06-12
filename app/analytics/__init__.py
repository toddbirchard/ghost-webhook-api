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
    weekly_traffic = top_visited_pages_by_timeframe("7d", limit=50)
    monthly_traffic = top_visited_pages_by_timeframe("30d", limit=100)
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
