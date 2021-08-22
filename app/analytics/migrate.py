"""Import site analytics from data warehouse to application."""
from pandas import DataFrame

from clients import gbq
from config import BASE_DIR
from database import rdbms


def import_site_analytics(timeframe: str) -> DataFrame:
    """
    Migrate raw analytics data from Google BigQuery to application db.

    :param timeframe: Timeframe to fetch data for (weekly, monthly, yearly).
    :type timeframe: str
    :returns: DataFrame
    """
    sql_query = open(f"{BASE_DIR}/database/queries/analytics/{timeframe}.sql").read()
    sql_table = f"{timeframe}_stats"
    query_job = gbq.query(sql_query)
    result = query_job.result()
    df = result.to_dataframe()
    result = rdbms.insert_dataframe(df, sql_table, "analytics", action="replace")
    return result
