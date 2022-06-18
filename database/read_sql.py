"""Read analytics from local SQL files."""
from os import listdir
from os.path import isfile, join
from typing import List

from config import BASE_DIR


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


def parse_sql_batch(sql_file_paths: List[str]) -> List[str]:
    """
    Read SQL analytics from .sql files.

    :param List[str] sql_file_paths: List of paths to SQL files to read and parse.

    :returns: List[str]
    """
    queries = []
    for file in sql_file_paths:
        sql_file = open(file, "r")
        query = sql_file.read()
        queries.append(query)
        sql_file.close()
    return queries
