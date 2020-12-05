from config import Settings

from .sql_db import Database

# Database connection
rdbms = Database(
    uri=Settings().SQLALCHEMY_DATABASE_URI, args=Settings().SQLALCHEMY_ENGINE_OPTIONS
)
