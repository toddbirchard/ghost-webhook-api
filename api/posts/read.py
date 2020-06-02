"""Read queries from local SQL files."""
from os import listdir
from os.path import isfile, join
from api.log import LOGGER


def get_queries():
    """Neatly package local queries to be run against database."""
    sql_file_paths = fetch_sql_files()
    sql_queries = read_sql_queries(sql_file_paths)
    sql_file_names = [file.split('/')[-1] for file in sql_file_paths]
    query_dict = dict(zip(sql_file_names, sql_queries))
    return query_dict


def fetch_sql_files():
    """Fetch all SQL query files in folder."""
    folder = 'api/posts/queries'
    directory = listdir(folder)
    files = [folder + '/' + f for f in directory if isfile(join(folder, f)) if '.sql' in f]
    LOGGER.info(f'Found {len(files)} queries from the `/queries` directory.')
    return files


def read_sql_queries(sql_file_paths):
    """Read SQL query from .sql file."""
    queries = []
    for file in sql_file_paths:
        sql_file = open(file, 'r')
        query = sql_file.read()
        queries.append(query)
        sql_file.close()
    return queries
