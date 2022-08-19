from sqlalchemy.engine.cursor import LegacyCursorResult

from database.read_sql import (
    collect_sql_queries,
    fetch_sql_files,
    parse_sql_batch
)
from log import LOGGER


def test_fetch_sql_files():
    """Get local SQL files containing DB queries."""
    files = fetch_sql_files("analytics")
    assert files is not None
    assert files[0].split(".")[1] == "sql"


def test_collect_sql_queries():
    """Create dict of SQL queries to be run where `keys` are filenames and `values` are queries."""
    queries = collect_sql_queries("analytics")
    assert type(queries) == dict


def test_select_query(ghost_db):
    posts_sql = fetch_sql_files("posts/selects")
    parsed_posts_sql = parse_sql_batch(posts_sql)
    query_result = ghost_db.execute_query(parsed_posts_sql[0])
    assert len(posts_sql) > 0
    assert type(parsed_posts_sql[0]) == str
    assert type(query_result) == LegacyCursorResult
    LOGGER.debug(query_result.rowcount)
