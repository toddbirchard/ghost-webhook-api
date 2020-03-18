"""Database client."""
from sqlalchemy import create_engine, MetaData, Table


class Database:

    def __init__(self, db_uri, db_args):
        self.engines = {
            'analytics': create_engine(db_uri + 'analytics', connect_args=db_args, echo=False),
            'blog': create_engine(db_uri + 'hackers_prod', connect_args=db_args, echo=False)
        }
        self.weekly_stats_table = Table('weekly_stats', MetaData(bind=self.engines['analytics']), autoload=True)
        self.monthly_stats_table = Table('monthly_stats', MetaData(bind=self.engines['analytics']), autoload=True)
        self.top_searches_table = Table('algolia_top_searches', MetaData(bind=self.engines['analytics']), autoload=True)
        self.tables = {'weekly_stats': self.weekly_stats_table,
                       'monthly_stats': self.monthly_stats_table,
                       'algolia_top_searches': self.top_searches_table}

    def run_query(self, sql_queries):
        """Execute SQL query."""
        results = {}
        for k, v in sql_queries.items():
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
        table = self.tables[table_name]
        self.engines['analytics'].execute(table.insert(), rows)
        return self.__construct_response(len(rows))

    @staticmethod
    def __construct_response(affected_rows):
        """Summarize results of an executed query."""
        return f'Modified {affected_rows} rows.'
