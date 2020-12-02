from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Settings

URI = Settings().SQLALCHEMY_DATABASE_URI
ARGS = Settings().SQLALCHEMY_ENGINE_OPTIONS

engine = create_engine(URI, connect_args=ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
