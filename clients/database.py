"""Database client."""
from typing import List, Optional
from pandas import DataFrame
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from clients.log import LOGGER


class Database:
    """Database client."""

    def __init__(
        self,
        uri: str,
        args: dict
    ):
        self.engines = {
            'analytics': create_engine(
                f'{uri}/analytics',
                connect_args=args,
                echo=False
            ),
            'hackers_prod': create_engine(
                f'{uri}/hackers_prod',
                connect_args=args,
                echo=False
            )
        }

    def _table(self, table_name: str, database_name='analytics') -> Table:
        return Table(
            table_name,
            MetaData(bind=self.engines[database_name]),
            autoload=True
        )

    @LOGGER.catch
    def execute_queries(self, queries: dict, database_name='hackers_prod') -> dict:
        """Execute SQL query."""
        results = {}
        for k, v in queries.items():
            query_result = self.engines[database_name].execute(v)
            results[k] = f'{query_result.rowcount} rows affected.'
        return results

    @LOGGER.catch
    def execute_query(self, query: str, database_name='hackers_prod'):
        """Execute single SQL query."""
        try:
            result = self.engines[database_name].execute(query)
            return result
        except SQLAlchemyError as e:
            LOGGER.error(e)
            return f'Failed to execute SQL query: {query}'

    @LOGGER.catch
    def execute_query_from_file(self, sql_file: str, database_name='hackers_prod'):
        """Execute single SQL query."""
        try:
            query = open(sql_file, 'r').read()
            result = self.engines[database_name].execute(query)
            return result
        except SQLAlchemyError as e:
            LOGGER.error(e)
            return f'Failed to execute SQL: {sql_file}'

    @LOGGER.catch
    def fetch_records(self, query, database_name=None) -> List[str]:
        """Fetch all rows via query."""
        rows = self.engines[database_name].execute(query).fetchall()
        return [row.items() for row in rows]

    @LOGGER.catch
    def fetch_record(self, query: str, database_name=None):
        """Fetch row via query."""
        return self.engines[database_name].execute(query).first()

    @LOGGER.catch
    def insert_records(self, rows, table_name=None, database_name=None, replace=None) -> str:
        """Insert rows into table."""
        try:
            if replace:
                self.engines[database_name].execute(f'TRUNCATE TABLE {table_name}')
            table = self._table(table_name)
            self.engines[database_name].execute(table.insert(), rows)
            return f'Inserted {len(rows)} into {table.name}.'
        except SQLAlchemyError as e:
            LOGGER.error(e)
            return f'Failed to insert rows.'

    def insert_dataframe(
            self,
            df: DataFrame,
            table_name=None,
            database_name='analytics',
            action='append'
    ):
        """Insert Pandas DataFrame into SQL table."""
        df.to_sql(table_name, self.engines[database_name], if_exists=action)
        return df.to_json(orient='records')
