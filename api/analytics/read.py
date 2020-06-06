"""Read queries from local SQL files."""


def read_sql_queries(file):
    """Read SQL query from .sql file."""
    file = open(f'api/analytics/queries/{file}', 'r')
    query = file.read()
    file.close()
    return query
