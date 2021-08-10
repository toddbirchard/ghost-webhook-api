"""Database client."""
from typing import List, Optional, Tuple

from pandas import DataFrame
from sqlalchemy import MetaData, Table, create_engine, text
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from log import LOGGER


class Database:
    """Database client."""

    def __init__(self, uri: str, args: dict):
        self.engines = {
            "analytics": create_engine(
                f"{uri}/analytics", connect_args=args, echo=False
            ),
            "hackers_prod": create_engine(
                f"{uri}/hackers_prod", connect_args=args, echo=False
            ),
        }

    def _table(self, table_name: str, database_name: str) -> Table:
        """
        :param str table_name: Name of database table to fetch
        :param str database_name: Name of database to connect to.

        :returns: Table
        """
        return Table(
            table_name, MetaData(bind=self.engines[database_name]), autoload=True
        )

    @LOGGER.catch
    def execute_queries(self, queries: dict, database_name: str) -> Tuple[dict, int]:
        """Execute collection of SQL analytics.

        :param dict queries: Map of query names -> SQL analytics.
        :param str database_name: Name of database to connect to.

        :returns: Tuple[dict, int]
        """
        results = {}
        total_rows = 0
        for k, v in queries.items():
            query_result = self.engines[database_name].execute(text(v))
            results[k] = query_result.rowcount
            total_rows += query_result.rowcount
        return results, total_rows

    @LOGGER.catch
    def execute_query(self, query: str, database_name: str) -> Optional[Result]:
        """
        Execute single SQL query.

        :param str query: SQL query to run against database.
        :param str database_name: Name of database to connect to.

        :returns: Optional[Result]
        """
        try:
            result = self.engines[database_name].execute(text(query))
            return result
        except SQLAlchemyError as e:
            LOGGER.error(f"Failed to execute SQL query {query}: {e}")

    @LOGGER.catch
    def execute_query_from_file(
        self, sql_file: str, database_name: str
    ) -> Optional[Result]:
        """
        Execute single SQL query.

        :param str sql_file: Filepath of SQL query to run.
        :param str database_name: Name of database to connect to.

        :returns: Optional[Result]
        """
        try:
            query = open(sql_file, "r").read()
            return self.engines[database_name].execute(query).fetchall()
        except SQLAlchemyError as e:
            LOGGER.error(f"Failed to execute SQL {sql_file}: {e}")

    @LOGGER.catch
    def fetch_records(self, query: str, database_name: str) -> Optional[List[str]]:
        """
        Fetch all rows via query.

        :param str query: SQL query to run against database.
        :param database_name: Name of database to connect to.

        :returns: Optional[List[str]]
        """
        rows = self.engines[database_name].execute(query).fetchall()
        if bool(rows):
            return [row.items() for row in rows]
        return None

    @LOGGER.catch
    def fetch_record(self, query: str, database_name: str) -> Optional[str]:
        """
        Fetch a single row; typically used to verify whether a
        record already exists (ie: users).

        :param str query: SQL query to run against database.
        :param str database_name: Name of database to connect to.

        :returns: Optional[str]
        """
        return self.engines[database_name].execute(query).first()

    def insert_records(
        self, rows: List[dict], table_name: str, database_name: str, replace=False
    ) -> Optional[int]:
        """
        Insert rows into SQL table.

        :param List[dict] rows: List of dictionaries to insert where keys are columns.
        :param str table_name: Name of database table to fetch.
        :param str database_name: Name of database to connect to.
        :param bool replace: Flag to truncate table prior to insert.

        :returns: Optional[int]
        """
        try:
            if replace:
                self.engines[database_name].execute(f"TRUNCATE TABLE {table_name}")
            table = self._table(table_name, database_name)
            self.engines[database_name].execute(table.insert(), rows)
            return len(rows)
        except SQLAlchemyError as e:
            LOGGER.error(f"SQLAlchemyError while inserting rows: {e}")
        except IntegrityError as e:
            LOGGER.error(f"IntegrityError while inserting rows: {e}")
        except Exception as e:
            LOGGER.error(f"Unexpected error while inserting rows: {e}")

    def insert_dataframe(
        self, df: DataFrame, table_name: str, database_name: str, action="append"
    ) -> DataFrame:
        """
        Insert Pandas DataFrame into SQL table.

        :param DataFrame df: Tabular data to insert into SQL table.
        :param str table_name: Name of database table to insert into.
        :param str database_name: Name of database to connect to.
        :param dtr action: Method of dealing with duplicate rows.

        :returns: DataFrame
        """
        df.to_sql(table_name, self.engines[database_name], if_exists=action)
        LOGGER.info(
            f"Updated {len(df)} rows via {action} into `{database_name}`.`{table_name}`."
        )
        return df
