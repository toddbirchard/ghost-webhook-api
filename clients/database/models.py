from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=False)
    user_name = Column(String, unique=False)
    user_avatar = Column(Text, unique=False)
    user_id = Column(String, unique=False, index=True)
    user_email = Column(String, unique=False)
    body = Column(Text, unique=False)
    created_at = Column(DateTime)
    post_slug = Column(String, unique=False)
    author_name = Column(String, unique=False)

    items = relationship("Item", back_populates="owner")
