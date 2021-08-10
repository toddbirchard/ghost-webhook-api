"""Database client."""
from typing import List, Optional, Tuple

from pandas import DataFrame
from sqlalchemy import MetaData, Table, text
from sqlalchemy.engine.result import Result, Row
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine
from config import Settings

from log import LOGGER


class Database:
    """Database client."""

    blog_engine = await create_async_engine(
        f"{Settings.SQLALCHEMY_DATABASE_URI}/analytics", connect_args=Settings.SQLALCHEMY_ENGINE_OPTIONS, echo=False
    )

    analytics_engine = await create_async_engine(
        f"{Settings.SQLALCHEMY_DATABASE_URI}/analytics", connect_args=Settings.SQLALCHEMY_ENGINE_OPTIONS, echo=False
    )

    async def _table(self, table_name: str, database_name: str) -> Table:
        """
        :param str table_name: Name of database table to fetch
        :param str database_name: Name of database to connect to.

        :returns: Table
        """
        async with self.engines[database_name].connect() as conn:
            table = await Table(
                table_name, MetaData(bind=conn), autoload=True
            )
            await conn.dispose()
            return table

    @LOGGER.catch
    async def execute_queries(self, queries: dict, database_name: str) -> Tuple[dict, int]:
        """
        Execute collection of SQL analytics.

        :param dict queries: Map of query names -> SQL analytics.
        :param str database_name: Name of database to connect to.

        :returns: Tuple[dict, int]
        """
        results = {}
        total_rows = 0
        for k, v in queries.items():
            async with self.blog_engine.connect() as conn:
                query_result = await self.blog_engine.execute(text(v))
                results[k] = query_result.rowcount
                total_rows += query_result.rowcount
                await conn.dispose()
        return results, total_rows

    @LOGGER.catch
    async def execute_query(self, query: str, database_name: str) -> Optional[Result]:
        """
        Execute single SQL query.

        :param str query: SQL query to run against database.
        :param str database_name: Name of database to connect to.

        :returns: Optional[Result]
        """
        try:
            async with self.blog_engine.connect() as conn:
                result = await conn.execute(text(query))
                await conn.dispose()
                return result
        except SQLAlchemyError as e:
            LOGGER.error(f"Failed to execute SQL query {query}: {e}")

    @LOGGER.catch
    async def execute_query_from_file(
        self, sql_file: str, database_name: str
    ) -> Optional[Result]:
        """
        Execute single SQL query.

        :param str sql_file: Filepath of SQL query to run.
        :param str database_name: Name of database to connect to.

        :returns: Optional[Result]
        """
        try:
            result = None
            query = open(sql_file, "r").read()
            async with self.blog_engine.connect() as conn:
                result = await conn.execute(query).fetchall()
                await conn.dispose()
            return result
        except SQLAlchemyError as e:
            LOGGER.error(f"Failed to execute SQL {sql_file}: {e}")

    @LOGGER.catch
    async def fetch_records(self, query: str, database_name: str) -> Optional[List[dict]]:
        """
        Fetch all rows via query.

        :param str query: SQL query to run against database.
        :param database_name: Name of database to connect to.

        :returns: Optional[List[dict]]
        """
        try:
            result = None
            async with self.blog_engine.connect() as conn:
                rows = await conn.execute(query).fetchall()
                result = [row.items() for row in rows]
                await conn.dispose()
                return result
        except SQLAlchemyError as e:
            LOGGER.error(f"SQLAlchemyError while fetching rows: {e}")
        except IntegrityError as e:
            LOGGER.error(f"IntegrityError while fetching rows: {e}")
        except Exception as e:
            LOGGER.error(f"Unexpected error while fetching rows: {e}")

    async def fetch_record(self, query: str, database_name: str) -> Optional[Result]:
        """
        Fetch a single row; typically used to verify whether a
        record already exists (ie: users).

        :param str query: SQL query to run against database.
        :param str database_name: Name of database to connect to.

        :returns: Optional[Result]
        """
        try:
            result = None
            async with self.blog_engine.connect() as conn:
                result = await conn.execute(query).first()
                await conn.dispose()
                return result
        except SQLAlchemyError as e:
            LOGGER.error(f"SQLAlchemyError while fetching rows: {e}")
        except IntegrityError as e:
            LOGGER.error(f"IntegrityError while fetching rows: {e}")
        except Exception as e:
            LOGGER.error(f"Unexpected error while fetching rows: {e}")

    async def insert_records(
        self, rows: List[dict], table_name: str, database_name: str, replace=False
    ) -> Optional[Result]:
        """
        Insert rows into SQL table.

        :param List[dict] rows: List of dictionaries to insert where keys are columns.
        :param str table_name: Name of database table to fetch.
        :param str database_name: Name of database to connect to.
        :param bool replace: Flag to truncate table prior to insert.

        :returns: Optional[Result]
        """
        try:
            result = None
            async with self.engines[database_name].connect() as conn:
                if replace:
                    conn.execute(f"TRUNCATE TABLE {table_name}")
                table = self._table(table_name, database_name)
                result = await conn.execute(table.insert(dialect="mysql"), rows)
                await conn.dispose()
            return result
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
        :param str action: Method of dealing with duplicate rows.

        :returns: DataFrame
        """
        df.to_sql(table_name, self.analytics_engine, if_exists=action)
        LOGGER.info(
            f"Updated {len(df)} rows via {action} into `{database_name}`.`{table_name}`."
        )
        return df
