import pytest

from config import settings
from database.sql_db import Database


@pytest.fixture
def rdbms():
    return Database(
        uri=settings.SQLALCHEMY_DATABASE_URI,
        hackers_db_name=settings.SQLALCHEMY_GHOST_DATABASE_NAME,
        features_db_name=settings.SQLALCHEMY_FEATURES_DATABASE_NAME,
        args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    )
