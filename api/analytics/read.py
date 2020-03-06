"""Read queries from local SQL files."""


def read_sql_queries(file):
    """Read SQL query from .sql file."""
    fd = open(f'api/analytics/queries/{file}', 'r')
    query = fd.read()
    fd.close()
    return query
