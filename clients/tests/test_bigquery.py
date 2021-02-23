from clients import gbq
from config import basedir


def test_fetch_weekly_bigquery():
    sql_query = open(f"{basedir}/database/queries/analytics/weekly.sql").read()
    results = gbq.query(sql_query).result()
    assert bool(results)
