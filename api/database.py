"""Database client."""
from sqlalchemy import create_engine, MetaData, Table, text


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

    def execute_query(self, query):
        """Execute single SQL query."""
        return self.engines['blog'].execute(query)

    def fetch_records(self, query, table_name='analytics'):
        """Fetch all rows via query."""
        rows = self.engines[table_name].execute(query).fetchall()
        return [{column: value for column, value in row.items()} for row in rows]

    def insert_records(self, rows, table_name, replace=None):
        """Insert rows into table."""
        if replace:
            self.engines['analytics'].execute(f'TRUNCATE TABLE {table_name}')
        table = self._table(table_name)
        self.engines['analytics'].execute(table.insert(), rows)
        return self._construct_response(len(rows))

    def update_post_image(self, image, post):
        """Set post feature image to desired image."""
        sql = f"UPDATE posts SET feature_image = '{image}' WHERE id = '{post}';"
        self.execute_query(sql)
        return {post: image}

    @staticmethod
    def _construct_response(affected_rows):
        """Summarize results of an executed query."""
        return f'Modified {affected_rows} rows.'
