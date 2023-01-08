from config import settings

from .sql_db import Database

# Ghost database connection
ghost_db = Database(
    uri=settings.SQLALCHEMY_DATABASE_URI,
    db_name=settings.SQLALCHEMY_GHOST_DATABASE_NAME,
    args=settings.SQLALCHEMY_ENGINE_OPTIONS,
)


# Feature database connection
feature_db = Database(
    uri=settings.SQLALCHEMY_DATABASE_URI,
    db_name=settings.SQLALCHEMY_FEATURES_DATABASE_NAME,
    args=settings.SQLALCHEMY_ENGINE_OPTIONS,
)
