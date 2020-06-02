"""BigQuery Client."""
from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData, Table


class BigQuery:
    """BigQuery Client."""

    def __init__(self, bigquery_uri):
        self.engine = create_engine(bigquery_uri)
        self.metadata = MetaData(bind=self.engine)
        self.table_name = None

    @property
    def table(self):
        """Load SQL table into DataFrame."""
        if self.table_name:
            return Table(self.table_name, self.metadata, autoload=True)
        return None

    def insert_rows(self, rows, table=None, replace=None):
        """Insert rows into table."""
        if replace:
            self.engine.execute(f'TRUNCATE TABLE {table}')
        self.table_name = table
        self.engine.execute(self.table.insert(), rows)
        return self.construct_response(rows, table)

    def fetch_rows(self, query):
        """Fetch all rows via query."""
        rows = self.engine.execute(query).fetchall()
        return rows

    @staticmethod
    def construct_response(rows, table):
        """Summarize results of an executed query."""
        columns = rows[0].keys()
        column_names = ", ".join(columns)
        return f'Inserted {len(rows)} rows into `{table}` with {len(columns)} columns: {column_names}'
