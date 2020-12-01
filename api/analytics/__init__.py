"""Fetch site traffic & search query analytics."""
from flask import current_app as api
from flask import make_response

from api.analytics.algolia import fetch_algolia_searches
from api.analytics.migrate import import_site_analytics
from clients import db


@api.route("/analytics", methods=["GET"])
def migrate_site_analytics():
    """Fetch top searches for weekly & monthly timeframes."""
    weekly_traffic = import_site_analytics("weekly")
    monthly_traffic = import_site_analytics("monthly")
    result = {
        "weekly_stats": f"{len(weekly_traffic)} rows",
        "monthly_traffic": f"{len(monthly_traffic)} rows",
    }
    return make_response(result, 200, {"content-type": "application/json"})


@api.route("/analytics/searches/week", methods=["GET"])
def week_searches():
    """Save top search queries for the current week."""
    records = fetch_algolia_searches(timeframe=7)
    rows = db.insert_records(
        records,
        "algolia_searches_week",
        "analytics",
        replace=True,
    )
    return make_response(
        f"Successfully inserted {rows} rows into `algolia_searches_week` table.", 200
    )


@api.route("/analytics/searches/historical", methods=["GET"])
def historical_searches():
    """Save and persist top search queries for the current month."""
    records = fetch_algolia_searches(timeframe=30)
    rows = db.insert_records(records, "algolia_searches_historical", "analytics")
    return make_response(
        f"Successfully inserted {rows} rows into `algolia_searches_historical` table.",
        200,
    )
