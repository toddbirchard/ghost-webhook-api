"""Test reading data directly form SQL databases."""
from sqlalchemy.engine.cursor import CursorResult

from database.read_sql import collect_sql_queries, fetch_sql_files, parse_sql_batch
from database.sql_db import Database
from log import LOGGER


def test_fetch_sql_files():
    """Get local SQL files containing DB queries."""
    files = fetch_sql_files("analytics")
    assert files is not None
    assert files[0].split(".")[1] == "sql"


def test_collect_sql_queries():
    """Structure dict of SQL queries to be run (k,v where k is `filename` and v is `query`)."""
    queries = collect_sql_queries("analytics")
    assert isinstance(queries, dict)


def test_select_query(ghost_db: Database):
    """
    Test fetching all posts from Ghost via SQL.

    :param Database ghost_db: Ghost database client.
    """
    posts_sql = fetch_sql_files("posts/selects")
    parsed_posts_sql = parse_sql_batch(posts_sql)
    query_result = ghost_db.execute_query(parsed_posts_sql[0])
    assert len(posts_sql) > 0
    assert isinstance(parsed_posts_sql[0], str)
    assert isinstance(query_result, CursorResult)
    LOGGER.debug(query_result.rowcount)
