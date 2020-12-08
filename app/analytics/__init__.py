"""Fetch site traffic & search query analytics."""
from fastapi import APIRouter

from app.analytics.algolia import fetch_algolia_searches
from app.analytics.migrate import import_site_analytics
from database import rdbms

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/")
def migrate_site_analytics():
    """Fetch top searches for weekly & monthly timeframes."""
    weekly_traffic = import_site_analytics("weekly")
    monthly_traffic = import_site_analytics("monthly")
    return {
        "weekly_stats": f"{weekly_traffic} rows",
        "monthly_traffic": f"{monthly_traffic} rows",
    }


@router.get("/searches/week")
def week_searches():
    """Save top search analytics for the current week."""
    records = fetch_algolia_searches(timeframe=7)
    rows = rdbms.insert_records(
        records,
        "algolia_searches_week",
        "analytics",
        replace=True,
    )
    return f"Successfully inserted {rows} rows into `algolia_searches_week` table."


@router.get("/searches/historical")
def historical_searches():
    """Save and persist top search analytics for the current month."""
    records = fetch_algolia_searches(timeframe=30)
    rows = rdbms.insert_records(records, "algolia_searches_historical", "analytics")
    return (
        f"Successfully inserted {rows} rows into `algolia_searches_historical` table."
    )
