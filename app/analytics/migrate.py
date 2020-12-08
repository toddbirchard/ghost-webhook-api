"""Import analytics from data warehouse to application."""
from clients import bigquery
from database import rdbms
from config import basedir


def import_site_analytics(timeframe: str) -> int:
    """
    Migrate raw analytics data from Google BigQuery to app Database.

    :param timeframe: Timeframe to fetch data for (weekly, monthly, yearly).
    :type timeframe: str
    """
    sql_query = open(f"{basedir}/database/queries/analytics/{timeframe}.sql").read()
    sql_table = f"{timeframe}_stats"
    results = bigquery.query(sql_query).result()
    df = results.to_dataframe()
    result = rdbms.insert_dataframe(df, sql_table, "analytics", action="replace")
    return result
