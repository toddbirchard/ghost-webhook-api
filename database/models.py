"""Data models."""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.orm import Base


class Comment(Base):
    """User-generated comment."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    user_name = Column(String(255), unique=False)
    user_avatar = Column(Text)
    user_id = Column(String(255), ForeignKey("accounts.netlify_id"), index=True, unique=False)
    user_email = Column(String(255))
    user_role = Column(String(255))
    body = Column(Text)
    post_slug = Column(String(191), ForeignKey("posts.slug"), index=True, unique=False)
    post_id = Column(String(24), ForeignKey("posts.id"), index=True, unique=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("Account", backref="user_id")

    def __repr__(self):
        return f"<Comment {self.id} from User={self.user_id} on Post={self.post_slug}>"


class CommentUpvote(Base):
    """Upvote for user comment."""

    __tablename__ = "comment_upvotes"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    account_id = Column(String(255), ForeignKey("accounts.id"), nullable=False)
    upvote = Column(Boolean, nullable=False)

    __table_args__ = (Index("upvote_index", "comment_id", "account_id", unique=True),)

    # Relationships
    comment = relationship("Comment", backref="comment_id")
    user = relationship("Account", backref="account_id")

    def __repr__(self):
        return f"<CommentUpvote {self.id} for Comment={self.comment_id} from Account={self.account_id}>"


class Account(Base):
    """Netlify-managed user account."""

    __tablename__ = "accounts"

    id = Column(String(255), primary_key=True, index=True)
    netlify_id = Column(String(255), index=True, unique=True, nullable=False)
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

    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    coffee_id = Column(Integer, unique=True, index=True)
    email = Column(String(255), unique=False, index=True)
    name = Column(String(255))
    count = Column(Integer)
    message = Column(Text)
    link = Column(Text, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Donation {self.id}, ({self.link}): `{self.message}`>"
