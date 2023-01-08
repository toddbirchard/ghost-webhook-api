"""Initialize database session."""
import databases
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

metadata = MetaData()

database = databases.Database(f"{settings.SQLALCHEMY_DATABASE_URI}/{settings.SQLALCHEMY_FEATURES_DATABASE_NAME}")

engine = create_engine(
    f"{settings.SQLALCHEMY_DATABASE_URI}/{settings.SQLALCHEMY_FEATURES_DATABASE_NAME}",
    connect_args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata.create_all(engine)


def get_db():
    ses = SessionLocal()
    try:
        yield ses
    finally:
        ses.close()
