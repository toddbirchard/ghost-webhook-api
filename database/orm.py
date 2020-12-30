from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Settings

URI = Settings().SQLALCHEMY_DATABASE_URI
ARGS = Settings().SQLALCHEMY_ENGINE_OPTIONS

engine = create_engine(f"{URI}/hackers_prod", connect_args=ARGS, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    ses = SessionLocal()
    try:
        yield ses
    finally:
        ses.close()
