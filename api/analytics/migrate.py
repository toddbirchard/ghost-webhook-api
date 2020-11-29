"""Import analytics from data warehouse to application."""
from clients import bigquery, db


def import_site_analytics(timeframe: str):
    """
    Migrate raw analytics data from Google BigQuery to app Database.

    :param timeframe: Colloquial timeframe to fetch data for (weekly, monthly, yearly).
    :type timeframe: str
    """
    sql_query = open(f"api/analytics/queries/{timeframe}.sql").read()
    sql_table = f"{timeframe}_stats"
    results = bigquery.query(sql_query).result()
    df = results.to_dataframe()
    result = db.insert_dataframe(df, sql_table, "analytics", action="replace")
    if result is None:
        return 0
    return result
