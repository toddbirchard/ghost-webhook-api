"""Fetch site traffic & search query analytics."""
import aiohttp
from fastapi import APIRouter, HTTPException

from app.analytics.algolia import fetch_algolia_searches, import_algolia_search_queries
from app.analytics.migrate import import_site_analytics
from config import settings
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
    """Fetch top searches for weekly & monthly timeframes."""
    weekly_traffic = import_site_analytics("weekly")
    monthly_traffic = import_site_analytics("monthly")
    LOGGER.success(
        f"Inserted {len(weekly_traffic)} rows into `weekly_stats`,  {len(monthly_traffic)}  into `monthly_stats`."
    )
    return {
        "updated": {
            "weekly_stats": {
                "count": len(weekly_traffic),
                "rows": {
                    zip(weekly_traffic.slug.tolist(), weekly_traffic.views.tolist())
                },
            },
            "monthly_stats": {
                "count": len(monthly_traffic),
                "rows": {
                    zip(monthly_traffic.slug.tolist(), monthly_traffic.views.tolist())
                },
            },
        }
    }


@router.get(
    "/searches/",
    summary="Import user search queries.",
    description="Store user search queries to a SQL database for analysis and suggestive search.",
    status_code=200,
)
async def save_user_search_queries():
    """Save top search analytics for the current week."""
    headers = {
        "x-algolia-application-id": settings.ALGOLIA_APP_ID,
        "x-algolia-api-key": settings.ALGOLIA_API_KEY,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        weekly_searches = await fetch_algolia_searches(session, 7)
        monthly_searches = await fetch_algolia_searches(session, 30)
        if weekly_searches is not None and monthly_searches is not None:
            weekly_searches = await import_algolia_search_queries(
                weekly_searches, "algolia_searches_week"
            )
            monthly_searches = await import_algolia_search_queries(
                monthly_searches, "algolia_searches_historical"
            )
            LOGGER.success(
                f"Inserted {len(weekly_searches)} rows into `algolia_searches_week`, \
                    {len(monthly_searches)} into `algolia_searches_historical."
            )
        else:
            raise HTTPException(500, "Unexpected error when saving search query data.")
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
