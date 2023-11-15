"""Initialize custom Database clients for direct read/write access."""
from config import Settings

from .sql_db import Database

# Ghost database connection
ghost_db = Database(
    uri=Settings().SQLALCHEMY_DATABASE_URI,
    db_name=Settings().SQLALCHEMY_GHOST_DATABASE_NAME,
    args=Settings().SQLALCHEMY_ENGINE_OPTIONS,
)


# Feature database connection
feature_db = Database(
    uri=Settings().SQLALCHEMY_DATABASE_URI,
    db_name=Settings().SQLALCHEMY_FEATURES_DATABASE_NAME,
    args=Settings().SQLALCHEMY_ENGINE_OPTIONS,
)
