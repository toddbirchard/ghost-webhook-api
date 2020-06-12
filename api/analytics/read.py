"""Read queries from local SQL files."""


def read_sql_queries(file):
    """Read SQL query from .sql file."""
    sql_file = open(f'api/analytics/queries/{file}', 'r')
    query = sql_file.read()
    sql_file.close()
    return query
