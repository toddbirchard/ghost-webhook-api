from config import Settings

from .sqldb import Database

# Database connection
rdbms = Database(
    uri=Settings().SQLALCHEMY_DATABASE_URI, args=Settings().SQLALCHEMY_ENGINE_OPTIONS
)
