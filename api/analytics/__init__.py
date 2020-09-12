"""Fetch site analytics data to determine trending posts."""
from flask import current_app as api
from flask import make_response
from clients import bigquery, db
from clients.log import LOGGER


@api.route('/analytics/week', methods=['GET'])
def analytics_week():
    """Fetch top searches for current week."""
    query = open('api/analytics/queries/top_pages_weekly.sql').read()
    results = bigquery.query(query).result()
    df = results.to_dataframe()
    result = db.insert_dataframe(
        df,
        table_name='weekly_stats',
        database_name='analytics',
        action='replace'
    )
    LOGGER.info(f'Successfully inserted {len(result)} rows into weekly_stats table.')
    return make_response(result, 200, {'content-type': 'application/json'})


@api.route('/analytics/month', methods=['GET'])
def analytics_month():
    """Fetch top searches for current month."""
    query = open('api/analytics/queries/top_pages_monthly.sql').read()
    results = bigquery.query(query).result()
    df = results.to_dataframe()
    result = db.insert_dataframe(
        df,
        table_name='monthly_stats',
        database_name='analytics',
        action='replace'
    )
    LOGGER.info(f'Successfully inserted {len(result)} rows into monthly_stats table.')
    return make_response(result, 200, {'content-type': 'application/json'})
