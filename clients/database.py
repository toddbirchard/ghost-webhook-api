"""Database client."""
from typing import List
from sqlalchemy import MetaData, Table
from clients.log import LOGGER
from flask_sqlalchemy import SQLAlchemy


class Database(SQLAlchemy):
    """Database client."""

    def __init__(self):
        super().__init__()

    @staticmethod
    def _table(database_name: str, table_name: str) -> Table:
        return Table(
            table_name,
            MetaData(bind=database_name),
            autoload=True
        )

    @LOGGER.catch
    def execute_queries(self, queries: dict) -> dict:
        """Execute SQL query."""
        results = {}
        engine = self.get_engine(bind='blog')
        for k, v in queries.items():
            query_result = engine.execute(v)
            results[k] = f'{query_result.rowcount} rows affected.'
        return results

    @LOGGER.catch
    def execute_query(self, query: str):
        """Execute single SQL query."""
        engine = self.get_engine(bind='blog')
        result = engine.execute(query)
        return result

    @LOGGER.catch
    def execute_query_from_file(self, sql_file: str):
        """Execute single SQL query."""
        engine = self.get_engine(bind='blog')
        query = open(sql_file, 'r').read()
        result = engine.execute(query, bind='blog')
        return result

    @LOGGER.catch
    def fetch_records(self, query, database_name='blog') -> List[str]:
        """Fetch all rows via query."""
        engine = self.get_engine(bind=database_name)
        rows = engine.execute(query).fetchall()
        return [row.items() for row in rows]

    @LOGGER.catch
    def fetch_record(self, query, database_name=None) -> str:
        """Fetch row via query."""
        engine = self.get_engine(bind=database_name)
        return engine.execute(query).fetch()

    @LOGGER.catch
    def insert_records(self, rows, database_name='analytics', table_name=None, replace=None):
        """Insert rows into table."""
        # engine = self.get_engine(bind=database_name)
        if replace:
            self.execute(f'TRUNCATE TABLE {table_name}', bind=database_name)
        table = self._table(database_name, table_name)
        table.insert()
        self.execute(table.insert(), rows, bind=database_name)
        return f'Inserted {len(rows)} into {table.name}.'

    @LOGGER.catch
    def update_post_image(self, image: str, post: str) -> dict:
        """Set post feature image to desired image."""
        sql = f"UPDATE posts SET feature_image = '{image}' WHERE id = '{post}';"
        self.execute_query(sql)
        return {post: image}

    def insert_dataframe(self, df, table_name=None, exists_action='append'):
        df.to_sql(table_name, self.get_engine(bind='analytics'), if_exists=exists_action)
        return df.to_json(orient='records')

    @staticmethod
    def _construct_response(affected_rows) -> str:
        """Summarize results of an executed query."""
        return f'Modified {affected_rows} rows.'
