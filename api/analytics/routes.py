from flask import current_app as api
from flask import jsonify, make_response
from api import gbq, db
from .read import read_sql_queries


@api.route('/analytics/week', methods=['GET'])
def analytics_week():
    """Fetch top searches for the current week."""
    query = read_sql_queries('top_pages_weekly.sql')
    rows = gbq.fetch_rows(query)
    results = db.insert_records(rows, 'weekly_stats', replace=True)
    return make_response(jsonify(results))


@api.route('/analytics/month', methods=['GET'])
def analytics_month():
    """Fetch top searches for the current month."""
    query = read_sql_queries('top_pages_monthly.sql')
    rows = gbq.fetch_rows(query)
    results = db.insert_records(rows, 'monthly_stats', replace=True)
    return make_response(jsonify(results))
