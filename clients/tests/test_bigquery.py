from clients import gbq
from config import BASE_DIR


def test_fetch_weekly_bigquery():
    sql_query = open(f"{BASE_DIR}/database/queries/analytics/weekly.sql").read()
    results = gbq.query(sql_query).result()
    assert bool(results)
