"""Fetch site analytics data to determine trending posts."""
from flask import current_app as api
from flask import make_response
from clients import bigquery, db
from clients.log import LOGGER


@LOGGER.catch
@api.route('/analytics/week', methods=['GET'])
def analytics_week():
    """Fetch top searches for current week."""
    query = open('api/analytics/queries/top_pages_weekly.sql').read()
    results = bigquery.query(query).result()
    df = results.to_dataframe()
    insert_result = db.insert_dataframe(
        df,
        table_name='weekly_stats',
        database_name='analytics',
        exists_action='replace'
    )
    return make_response(insert_result, 200, {'content-type': 'application/json'})


@LOGGER.catch
@api.route('/analytics/month', methods=['GET'])
def analytics_month():
    """Fetch top searches for current month."""
    query = open('api/analytics/queries/top_pages_monthly.sql').read()
    results = bigquery.query(query).result()
    df = results.to_dataframe()
    insert_result = db.insert_dataframe(
        df,
        table_name='monthly_stats',
        database_name='analytics',
        exists_action='replace'
    )
    return make_response(insert_result, 200, {'content-type': 'application/json'})
