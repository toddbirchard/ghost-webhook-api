"""Data models."""
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import FetchedValue

Base = declarative_base()


class Account(Base):
    """User account."""

    __tablename__ = "account"

    id = Column(String(255), primary_key=True, index=True)
    full_name = Column(String(255))
    avatar_url = Column(Text, unique=False)
    email = Column(String(255), index=True, unique=True)
    role = Column(String(255), unique=False, nullable=True)
    provider = Column(String(255), unique=False)
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime, onupdate=FetchedValue())

    def __repr__(self):
        return f"<Account id={self.id}, name={self.full_name}, email={self.email}>"


class Donation(Base):
    """BuyMeACoffee donation."""

    __tablename__ = "donation"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    coffee_id = Column(Integer, unique=True)
    email = Column(String(255), unique=False, index=True)
    name = Column(String(255))
    count = Column(Integer)
    message = Column(Text)
    url = Column(Text, unique=True, index=True)
    created_at = Column(DateTime, server_default=FetchedValue())

    def __repr__(self):
        return f"<Donation {self.id}, ({self.url}): `{self.message}`>"
