import pytest

from config import Settings
from database.sql_db import Database


@pytest.fixture
def rdbms():
    return Database(
        uri=Settings().SQLALCHEMY_DATABASE_URI,
        args=Settings().SQLALCHEMY_ENGINE_OPTIONS,
    )
