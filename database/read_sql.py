"""Read analytics from local SQL files."""
from os import listdir
from os.path import isfile, join
from typing import List, Optional

from config import settings
from log import LOGGER


def collect_sql_queries(subdirectory: str) -> dict:
    """
    Create dict of SQL queries to be run where `keys` are filenames and `values` are queries.

    :param subdirectory: Directory containing .sql queries to run in bulk.

    :returns: dict
    """
    sql_file_paths = fetch_sql_files(subdirectory)
    sql_queries = parse_sql_batch(sql_file_paths)
    sql_file_names = [file.split("/")[-1] for file in sql_file_paths]
    query_dict = dict(zip(sql_file_names, sql_queries))
    return query_dict


def fetch_sql_files(subdirectory: str) -> List[Optional[str]]:
    """
    Fetch all `.sql` files in local folder.

    :param str subdirectory: Subdirectory containing SQL files to fetch.

    :returns: List[Optional[str]]
    """
    folder = f"{settings.BASE_DIR}/database/queries/{subdirectory}"
    directory = listdir(folder)
    LOGGER.info(f"Fetching SQL files from {subdirectory}")
    return [f"{folder}/{f}" for f in directory if isfile(join(folder, f)) if ".sql" in f]


def parse_sql_batch(sql_file_paths: List[str]) -> List[str]:
    """
    Read SQL analytics from .sql files.

    :param List[str] sql_file_paths: List of paths to SQL files to read and parse.

    :returns: List[str]
    """
    queries = []
    print(f"sql_file_paths = {sql_file_paths}")
    for file in sql_file_paths:
        with open(file, "r", encoding="utf-8") as f:
            query = f.read()
            queries.append(query)
    return queries
