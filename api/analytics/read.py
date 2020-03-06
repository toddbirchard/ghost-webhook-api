def read_sql_queries(file):
    """Read SQL query from .sql file."""
    fd = open('api/analytics/queries/' + file, 'r')
    query = fd.read()
    fd.close()
    return query
