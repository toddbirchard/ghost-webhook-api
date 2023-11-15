"""Test BigQuery client."""
from google.cloud import bigquery
from google.cloud.bigquery.table import RowIterator

from config import settings


def test_fetch_weekly_bigquery(gbq: bigquery):
    """
    Test fetching weekly Algolia search data from BigQuery.

    :param bigquery gbq: Test client for BigQuery.
    """
    with open(f"{settings.BASE_DIR}/database/queries/analytics/weekly.sql", encoding="utf-8") as f:
        sql_query = f.read()
        results = gbq.query(sql_query).result()
        assert bool(results)
        assert isinstance(results, RowIterator)
        assert results.total_rows >= 0
