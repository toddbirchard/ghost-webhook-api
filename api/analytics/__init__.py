"""Fetch site analytics data to determine trending posts."""
from flask import current_app as api
from flask import jsonify, make_response
from api import gbq, db
from api.log import LOGGER


@LOGGER.catch
@api.route('/analytics/week', methods=['GET'])
def analytics_week():
    """Fetch top searches for the current week."""
    query = gbq.parse_query_from_file('api/analytics/queries/top_pages_weekly.sql')
    rows = gbq.fetch_rows(query)
    results = db.insert_records(rows, 'weekly_stats', replace=True)
    LOGGER.info(results)
    return make_response(jsonify(results))


@LOGGER.catch
@api.route('/analytics/month', methods=['GET'])
def analytics_month():
    """Fetch top searches for the current month."""
    query = gbq.parse_query_from_file('api/analytics/queries/top_pages_monthly.sql')
    rows = gbq.fetch_rows(query)
    results = db.insert_records(rows, 'monthly_stats', replace=True)
    LOGGER.info(results)
    return make_response(jsonify(results))
