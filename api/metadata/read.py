"""Read SQL files."""
from sys import stdout
from os import listdir
from os.path import isfile, join
from loguru import logger

logger.add(stdout, format="{time} {message}", level="INFO", filter="queries")


def get_queries():
    """Neatly package local queries to be run against database."""
    files = fetch_sql_files()
    sql = read_sql_queries(files)
    query_dict = dict(zip(files, sql))
    return query_dict


def fetch_sql_files():
    """Fetch all SQL query files in folder."""
    folder = 'api/metadata/queries'
    directory = listdir(folder)
    files = [folder + '/' + f for f in directory if isfile(join(folder, f)) if '.sql' in f]
    logger.info(f'Found {len(files)} queries from the `/queries` directory.')
    return files


def read_sql_queries(files):
    """Read SQL query from .sql file."""
    queries = []
    for file in files:
        fd = open(file, 'r')
        query = fd.read()
        queries.append(query)
        fd.close()
    return queries
