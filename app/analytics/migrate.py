"""Import site analytics from data warehouse to application."""
from typing import Any, Dict, List

from clients import gbq
from config import settings
from database import feature_db


def import_site_analytics(timeframe: str) -> Dict[str, List[Any]]:
    """
    Migrate raw analytics data from Google BigQuery to application db.

    :param str timeframe: Time frame to fetch data for (weekly, monthly, yearly).

    :returns: Dict[str, List[Any]]
    """
    sql_query = open(f"{settings.BASE_DIR}/database/queries/analytics/{timeframe}.sql").read()
    sql_table = f"{timeframe}_stats"
    query_job = gbq.query(sql_query)
    result = query_job.result()
    df = result.to_dataframe()
    result = feature_db.insert_dataframe(df, sql_table, action="replace")
    return {"posts": result["slug"].to_list(), "views": result["views"].to_list()}
