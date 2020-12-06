"""Read queries from local SQL files."""
from os import listdir
from os.path import isfile, join
from typing import List

from clients.log import LOGGER
from config import basedir
from database import rdbms


def collect_sql_queries() -> dict:
    """Create dict of queries to be run against database."""
    sql_file_paths = fetch_sql_files()
    sql_queries = parse_sql_batch(sql_file_paths)
    sql_file_names = [file.split("/")[-1] for file in sql_file_paths]
    query_dict = dict(zip(sql_file_names, sql_queries))
    return query_dict


def fetch_sql_files(subdirectory: str = "") -> List[str]:
    """Fetch all SQL query files in folder."""
    folder = f"{basedir}/app/posts/queries{subdirectory}"
    directory = listdir(folder)
    files = [
        folder + "/" + f for f in directory if isfile(join(folder, f)) if ".sql" in f
    ]
    LOGGER.info(f"Found {len(files)} queries in `{folder}`.")
    return files


def parse_sql_batch(sql_file_paths: List) -> List[str]:
    """Read SQL queries from .sql files."""
    queries = []
    for file in sql_file_paths:
        sql_file = open(file, "r")
        query = sql_file.read()
        queries.append(query)
        sql_file.close()
    return queries


def fetch_raw_lynx_posts():
    """Find all Lynx posts lacking embedded link previews."""
    sql_file = open(f"{basedir}/app/posts/queries/selects/lynx_bookmarks.sql", "r")
    query = sql_file.read()
    posts = rdbms.execute_query(query, "hackers_prod").fetchall()
    return posts
