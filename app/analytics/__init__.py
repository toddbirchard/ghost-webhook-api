"""Fetch site traffic & search query analytics."""
from fastapi import APIRouter

from app.analytics.algolia import fetch_algolia_searches
from app.analytics.migrate import import_site_analytics
from clients.log import LOGGER
from database import rdbms

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/")
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


@router.get("/searches/week")
async def week_searches():
    """Save top search analytics for the current week."""
    records = fetch_algolia_searches(timeframe=7)
    rows = rdbms.insert_records(
        records,
        "algolia_searches_week",
        "analytics",
        replace=True,
    )
    LOGGER.success(f"Inserted {rows} rows into `algolia_searches_week` table.")
    return f"Successfully inserted {rows} rows into `algolia_searches_week` table."


@router.get("/searches/historical")
async def historical_searches():
    """Save and persist top search analytics for the current month."""
    records = fetch_algolia_searches(timeframe=30)
    rows = rdbms.insert_records(records, "algolia_searches_historical", "analytics")
    LOGGER.success(f"Inserted {rows} rows into `algolia_searches_week` table.")
    return (
        f"Successfully inserted {rows} rows into `algolia_searches_historical` table."
    )
