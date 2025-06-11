"""Initialize custom Database clients for direct read/write access."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import Settings, settings

from .sql_db import Database

# Create SQL Engine
engine = create_engine(
    f"{settings.SQLALCHEMY_DATABASE_URI}/{settings.SQLALCHEMY_FEATURES_DATABASE_NAME}",
    connect_args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    echo=False,
)

# Create SQL Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Database session dependency
def get_db():
    ses = SessionLocal()
    try:
        yield ses
    finally:
        ses.close()


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
