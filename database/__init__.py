from config import Settings

from .sql_db import Database

# Database connection
rdbms = Database(
    uri=Settings().SQLALCHEMY_DATABASE_URI,
    hackers_db_name=Settings().SQLALCHEMY_GHOST_DATABASE_NAME,
    features_db_name=Settings().SQLALCHEMY_FEATURES_DATABASE_NAME,
    args=Settings().SQLALCHEMY_ENGINE_OPTIONS,
)
