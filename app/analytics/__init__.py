"""Fetch site traffic & search query analytics."""
from fastapi import APIRouter, HTTPException

from app.analytics.algolia import fetch_algolia_searches, import_algolia_search_queries
from app.analytics.migrate import import_site_analytics
from database.schemas import AnalyticsResponse
from clients.log import LOGGER

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/",
    summary="Import site analytics.",
    description="Import site performance analytics from a data warehouse to a SQL database.",
    response_model=AnalyticsResponse
)
async def migrate_site_analytics():
    """Fetch top searches for weekly & monthly timeframes."""
    weekly_traffic = import_site_analytics("weekly")
    monthly_traffic = import_site_analytics("monthly")
    LOGGER.success(
        f"Inserted {len(weekly_traffic)} rows into `weekly_stats`,  {len(monthly_traffic)}  into `monthly_stats`."
    )
    return {
        "weekly_stats": {
            "count": len(weekly_traffic),
            "rows": {zip(weekly_traffic.slug.tolist(), weekly_traffic.views.tolist())},
        },
        "monthly_traffic": {
            "count": len(monthly_traffic),
            "rows": {
                zip(monthly_traffic.slug.tolist(), monthly_traffic.views.tolist())
            },
        },
    }


@router.get("/searches/")
async def save_user_search_queries():
    """Save top search analytics for the current week."""
    weekly_searches = fetch_algolia_searches(7)
    monthly_searches = fetch_algolia_searches(30)
    if weekly_searches is None and monthly_searches is None:
        HTTPException(500, "Unexpected error when saving search query data.")
    import_algolia_search_queries(weekly_searches, "algolia_searches_week")
    import_algolia_search_queries(monthly_searches, "algolia_searches_historical")
    LOGGER.success(
        f"Inserted {len(weekly_searches)} rows into `algolia_searches_week`, \
            {len(monthly_searches)} into `algolia_searches_historical."
    )
    return {
        "weekly_queries": {
            "count": len(weekly_searches),
            "rows": weekly_searches,
        },
        "monthly_queries": {
            "count": len(monthly_searches),
            "rows": monthly_searches,
        },
    }
