"""Data models."""
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

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
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Account {self.id}, {self.full_name}, {self.email}>"


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
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Donation {self.id}, ({self.url}): `{self.message}`>"


class TrendingPostInsight(Base):
    """."""

    __tablename__ = "trending_post_insight"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    title = Column(Text)
    slug = Column(String(255))
    url = Column(String(255))
    page_views = Column(Integer)
    unique_visitors = Column(Integer)
    avg_visit_duration_secs = Column(Integer)
    bounce_rate_pct = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<TrendingPageInsight {self.id}, ({self.url}): `{self.message}`>"
