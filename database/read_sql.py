"""Read analytics from local SQL files."""
from os import listdir
from os.path import isfile, join
from typing import List

from sqlalchemy.engine.result import Result

from config import BASE_DIR
from database import rdbms


def collect_sql_queries(subdirectory: str) -> List[dict]:
    """
    Create dict of SQL queries to be run where `keys` are filenames and `values` are queries.

    :param str subdirectory: Directory containing .sql queries to run in bulk.

    :returns: List[dict]
    """
    sql_file_paths = fetch_sql_files(subdirectory)
    sql_queries = parse_sql_batch(sql_file_paths)
    return sql_queries


def fetch_sql_files(subdirectory: str) -> List[str]:
    """
    Fetch all SQL query files in folder.

    :param str subdirectory: Subdirectory containing SQL files to fetch.

    :returns: List[str]
    """
    folder = f"{BASE_DIR}/database/queries/{subdirectory}"
    directory = listdir(folder)
    files = [
        folder + "/" + f for f in directory if isfile(join(folder, f)) if ".sql" in f
    ]
    return files


def parse_sql_batch(sql_file_paths: List[str]) -> List[dict]:
    """
    Read SQL analytics from .sql files.

    :param List[str] sql_file_paths: List of paths to SQL files to read and parse.

    :returns: List[dict]
    """
    queries = []
    for file in sql_file_paths:
        sql_file = open(file, "r")
        query = sql_file.read()
        query_dict = {file.split("/")[-1]: query}
        queries.append(query_dict)
        sql_file.close()
    return queries


def fetch_raw_lynx_posts() -> Result:
    """
    Find all Lynx posts lacking embedded link previews.

    :returns: Result
    """
    sql_file = open(
        f"{BASE_DIR}/database/queries/posts/selects/lynx_bookmarks.sql", "r"
    )
    query = sql_file.read()
    posts = rdbms.execute_query(query, "hackers_prod").all()
    return posts
