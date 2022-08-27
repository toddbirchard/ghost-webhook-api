"""Database client."""
from typing import List, Optional, Union

from pandas import DataFrame
from sqlalchemy import MetaData, Table, create_engine, text
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from log import LOGGER


class Database:
    """Database client."""

    def __init__(self, uri: str, db_name: str, args: dict):
        self.db = create_engine(f"{uri}/{db_name}", connect_args=args, echo=False)

    def _table(self, table_name: str) -> Table:
        """
        Build database table object.

        :param str table_name: Name of database table to fetch

        :returns: Table
        """
        return Table(table_name, MetaData(bind=self.db), autoload=True)

    def execute_queries(self, queries: dict) -> Optional[dict]:
        """
        Execute collection of SQL analytics.

        :param dict queries: Map of query names -> SQL analytics.

        :returns: Optional[dict]
        """
        try:
            results = {}
            for k, v in queries.items():
                query_result = self.db.execute(v)
                results[k] = f"{query_result.rowcount} rows affected."
            return results
        except SQLAlchemyError as e:
            LOGGER.error(f"SQLAlchemyError while executing queries `{','.join(queries.keys())}`: {e}")
            return None
        except Exception as e:
            LOGGER.error(f"Unexpected exception while executing queries `{','.join(queries.keys())}`: {e}")
            return None

    def execute_query(self, query: str) -> Optional[Result]:
        """
        Execute single SQL query.

        :param str query: SQL query to run against database.

        :returns: Optional[Result]
        """
        try:
            result = self.db.execute(query)
            return result
        except SQLAlchemyError as e:
            LOGGER.error(f"Failed to execute SQL query {query}: {e}")
            return None

    def execute_query_from_file(self, sql_file: str) -> Union[List[dict], str]:
        """
        Execute single SQL query.

        :param str sql_file: Filepath of SQL query to run.

        :returns: Union[List[dict], str]
        """
        try:
            with self.db.connect() as conn:
                query = open(sql_file, "r").read()
                LOGGER.info(f"query={query}")
                results = conn.execute(text(query)).fetchall()
                return [dict(r) for r in results]
        except SQLAlchemyError as e:
            LOGGER.error(f"SQLAlchemyError while executing SQL `{sql_file}`: {e}")
            return f"Failed to execute SQL `{sql_file}`: {e}"
        except Exception as e:
            LOGGER.error(f"Unexpected exception while executing SQL `{sql_file}`: {e}")
            return f"Failed to execute SQL `{sql_file}`: {e}"

    def insert_records(self, rows: List[dict], table_name: str, replace=False) -> Optional[Result]:
        """
        Insert rows into SQL table.

        :param List[dict] rows: List of dictionaries to insert where keys are columns.
        :param str table_name: Name of database table to fetch.
        :param bool replace: Flag to truncate table prior to insert.

        :returns: Optional[Result]
        """
        try:
            if replace:
                self.db.execute(f"TRUNCATE TABLE {table_name}")
            table = self._table(table_name)
            return self.db.execute(table.insert(), rows)
        except IntegrityError as e:
            LOGGER.error(f"Unexpected error while inserting records into table `{table_name}`: {e}")
            return None
        except SQLAlchemyError as e:
            LOGGER.error(f"SQLAlchemyError while inserting records into table `{table_name}`: {e}")
            return None

    def insert_dataframe(self, df: DataFrame, table_name: str, action="append") -> DataFrame:
        """
        Insert Pandas DataFrame into SQL table.

        :param DataFrame df: Tabular data to insert into SQL table.
        :param str table_name: Name of database table to insert into.
        :param str action: Method of dealing with duplicate rows.

        :returns: DataFrame
        """
        df.to_sql(table_name, self.db, if_exists=action)
        LOGGER.info(f"Updated {len(df)} rows via {action} into `{table_name}`.")
        return df
