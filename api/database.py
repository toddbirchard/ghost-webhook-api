from sqlalchemy import create_engine, MetaData
from api import logger


class Database:
    """Database connection class."""

    def __init__(self, db_uri, db_args):
        self.engine = create_engine(db_uri,
                                    connect_args=db_args,
                                    echo=False)
        self.metadata = MetaData(bind=self.engine)

    def run_query(self, sql_queries):
        """Execute SQL query."""
        affected_rows = 0
        for k, v in sql_queries.items():
            logger.info(f'Executing query: {k}')
            if 'SELECT' in v:
                results = self.engine.execute(v).fetchall()
                affected_rows = len(results)
            results = self.engine.execute(v)
            affected_rows = results.rowcount
            logger.info(f'Modified {affected_rows} rows.')
        return self.__construct_response(affected_rows)

    def insert_records(self, record_dict):
        """Insert list of dicts into table."""
        self.engine.execute(self.table.insert(), record_dict)
        return self.__construct_response(record_dict, self.table)

    @staticmethod
    def __construct_response(affected_rows):
        """Summarize results of an executed query."""
        return f'Modified {affected_rows} rows.'
