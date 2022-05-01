from google.cloud.bigquery.table import RowIterator

from config import BASE_DIR


def test_fetch_weekly_bigquery(gbq):
    sql_query = open(f"{BASE_DIR}/database/queries/analytics/weekly.sql").read()
    results = gbq.query(sql_query).result()
    assert bool(results)
    assert type(results) == RowIterator
    assert results.total_rows > 0
