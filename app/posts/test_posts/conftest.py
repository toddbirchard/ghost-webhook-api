"""Set up integration tests for Ghost post modifications directly via SQL."""

import pytest

from config import settings
from database.sql_db import Database


@pytest.fixture
def ghost_db() -> Database:
    """
    Ghost database client.

    :returns: Database
    """
    return Database(
        uri=settings.SQLALCHEMY_DATABASE_URI,
        db_name=settings.SQLALCHEMY_GHOST_DATABASE_NAME,
        args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    )


@pytest.fixture
def feature_db() -> Database:
    """
    Added functionality database client.

    :returns: Database
    """
    return Database(
        uri=settings.SQLALCHEMY_DATABASE_URI,
        db_name=settings.SQLALCHEMY_FEATURES_DATABASE_NAME,
        args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    )
