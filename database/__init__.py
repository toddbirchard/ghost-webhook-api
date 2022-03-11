from config import Settings

from .sql_db import SQLDatabase

# Database connection
rdbms = SQLDatabase(
    uri=Settings().SQLALCHEMY_DATABASE_URI, 
    args=Settings().SQLALCHEMY_ENGINE_OPTIONS
)
