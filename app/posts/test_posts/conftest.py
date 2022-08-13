import pytest

from config import settings
from database.sql_db import Database


@pytest.fixture
def ghost_db():
    return Database(
        uri=settings.SQLALCHEMY_DATABASE_URI,
        db_name=settings.SQLALCHEMY_GHOST_DATABASE_NAME,
        args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    )


@pytest.fixture
def feature_db():
    return Database(
        uri=settings.SQLALCHEMY_DATABASE_URI,
        db_name=settings.SQLALCHEMY_FEATURES_DATABASE_NAME,
        args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    )
