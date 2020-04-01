"""Database client."""
from sqlalchemy import create_engine, MetaData, Table


class Database:

    def __init__(self, db_uri, db_args):
        self.engines = {
            'analytics': create_engine(db_uri + 'analytics', connect_args=db_args, echo=False),
            'blog': create_engine(db_uri + 'hackers_prod', connect_args=db_args, echo=False)
        }

    def _table(self, table_name):
        return Table(table_name, MetaData(bind=self.engines['analytics']), autoload=True)

    def execute_queries(self, queries):
        """Execute SQL query."""
        results = {}
        for k, v in queries.items():
            query_result = self.engines['blog'].execute(v)
            results[k] = f'{query_result.rowcount} rows affected.'
        return results

    def fetch_records(self, query):
        """Fetch all rows via query."""
        rows = self.engines['analytics'].execute(query).fetchall()
        return rows

    def insert_records(self, rows, table_name, replace=None):
        """Insert rows into table."""
        if replace:
            self.engines['analytics'].execute(f'TRUNCATE TABLE {table_name}')
        table = self._table(table_name)
        self.engines['analytics'].execute(table.insert(), rows)
        return self._construct_response(len(rows))

    @staticmethod
    def _construct_response(affected_rows):
        """Summarize results of an executed query."""
        return f'Modified {affected_rows} rows.'
