from sqlalchemy import Column, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from .orm import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(String(255), unique=True)
    email = Column(String(255), unique=False)
    user_name = Column(String(255), unique=False)
    user_avatar = Column(Text, unique=False)
    user_id = Column(String(255), unique=False, index=True)
    user_email = Column(String(255), unique=False)
    body = Column(Text, unique=False)
    created_at = Column(DateTime)
    post_slug = Column(String(255), unique=False)
    author_name = Column(String(255), unique=False)


class Donation(Base):
    __tablename__ = "donation"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=False)
    name = Column(String(255), unique=False)
    count = Column(Integer, unique=False)
    message = Column(Text, unique=False)
    link = Column(String(255), unique=True)
    created_at = Column(DateTime)
    coffee_id = Column(Integer, unique=True)
