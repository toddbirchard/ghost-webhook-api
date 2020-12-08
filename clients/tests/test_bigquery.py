import pytest
from config import basedir
from clients import bigquery


def test_fetch_weekly_bigquery():
    sql_query = open(f"{basedir}/database/queries/analytics/weekly.sql").read()
    results = bigquery.query(sql_query).result()
    assert bool(results)
