from datetime import datetime
from typing import Optional

from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database.models import Account, Comment, CommentUpvote, Donation
from database.schemas import NetlifyAccount, NewComment, NewDonation
from log import LOGGER


def get_donation(db: Session, donation: NewDonation) -> Optional[NewDonation]:
    """
    Fetch BuyMeACoffee donation by ID.

    :param Session db: ORM database session.
    :param NewDonation donation: Donation record to be fetched.

    :returns: Optional[NewDonation]
    """
    existing_donation = db.query(Donation).filter(Donation.coffee_id == donation.coffee_id).first()
    if existing_donation is None:
        return donation
    LOGGER.warning(f"Donation `{existing_donation.id}` from `{existing_donation.email}` already exists; skipping.")
    return None


def create_donation(db: Session, donation: NewDonation) -> Donation:
    """
    Create new BuyMeACoffee donation record.

    :param Session db: ORM database session.
    :param NewDonation donation: Donation schema object.

    :returns: Donation
    """
    try:
        db_item = Donation(
            coffee_id=donation.coffee_id,
            email=donation.email,
            name=donation.name,
            count=donation.count,
            message=donation.message,
            link=donation.link,
            created_at=datetime.now(),
        )
        db.add(db_item)
        db.commit()
        LOGGER.success(f"Successfully received donation: `{donation.count}` coffees from `{donation.name}`.")
        return db_item
    except IntegrityError as e:
        LOGGER.error(f"DB IntegrityError while creating donation record: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while creating donation record: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while creating donation record: {e}")


def get_comment(db: Session, comment_id: int) -> Optional[Result]:
    """
    Fetch BuyMeACoffee donation by ID.

    :param Session db: ORM database session.
    :param int comment_id: Primary key for user comment record.

    :returns: Optional[Result]
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


def create_comment(db: Session, comment: NewComment, user_role: Optional[str]) -> Comment:
    """
    Create new user-submitted comment.

    :param Session db: ORM database session.
    :param NewComment comment: User comment object.
    :param Optional[str] user_role: Permissions of the comment author, if any.

    :returns: Comment
    """
    try:
        LOGGER.info(f"Creating comment from {comment.user_email} on {comment.post_slug}...")
        new_comment = Comment(
            user_id=comment.user_id,
            user_name=comment.user_name,
            user_avatar=comment.user_avatar,
            user_email=comment.user_email,
            user_role=user_role,
            body=comment.body,
            post_slug=comment.post_slug,
            post_id=comment.post_id,
            created_at=datetime.now(),
        )
        db.add(new_comment)
        db.commit()
        LOGGER.success(f"New comment created by user `{new_comment.user_name}` on post `{new_comment.post_slug}`")
        return new_comment
    except IntegrityError as e:
        LOGGER.error(f"DB IntegrityError while creating comment: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while creating comment: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while creating comment: {e}")


def submit_comment_upvote(db: Session, user_id: str, comment_id: int) -> CommentUpvote:
    """
     Create a record of a user's upvote for a given comment.

     :param Session db: ORM database session.
     :param str user_id: Primary key for account record.
     :param int comment_id: Unique ID of comment user attempted to upvote.

    :returns: CommentUpvote
    """
    try:
        upvote = CommentUpvote(user_id=user_id, comment_id=comment_id)
        db.add(upvote)
        db.commit()
        LOGGER.success(f"Upvote submitted for comment `{comment_id}` from user `{user_id}`.")
        return upvote
    except IntegrityError as e:
        LOGGER.error(f"DB IntegrityError while registering comment upvote: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while registering comment upvote: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while registering comment upvote: {e}")


def remove_comment_upvote(db: Session, user_id: str, comment_id: int):
    """
    Delete a record of a user's upvote for a given comment.

    :param Session db: ORM database session.
    :param str user_id: Primary key for account record.
    :param int comment_id: Unique ID of comment user attempted to upvote.

    :returns: CommentUpvote
    """
    try:
        upvote = CommentUpvote(user_id=user_id, comment_id=comment_id)
        db.delete(upvote)
        db.commit()
        LOGGER.success(f"Removed upvote for comment `{comment_id}` from user `{user_id}`.")
    except IntegrityError as e:
        LOGGER.error(f"DB IntegrityError while attempting to remove comment upvote: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while attempting to remove comment upvote: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while attempting to remove comment upvote: {e}")


def get_comment_upvote(db: Session, user_id: str, comment_id: int) -> Optional[Result]:
    """
    Validate whether a user has upvoted a given comment.

    :param Session db: ORM database session.
    :param str user_id: Primary key for account record.
    :param int comment_id: Unique ID of comment user attempted to upvote.

    :returns: Optional[Result]
    """
    return (
        db.query(CommentUpvote)
        .filter(CommentUpvote.user_id == user_id and CommentUpvote.comment_id == comment_id)
        .first()
    )


def get_account(db: Session, account_email: str) -> Optional[Result]:
    """
    Fetch account by email address.

    :param Session db: ORM database session.
    :param str account_email: Primary key for account record.

    :returns: Optional[Result]
    """
    return db.query(Account).filter(Account.email == account_email).first()


def create_account(db: Session, account: NetlifyAccount) -> NetlifyAccount:
    """
    Create new account record sourced from Netlify.

    :param Session db: ORM database session.
    :param account: User comment schema object.
    :param NetlifyAccount account: User account registered via Netlify.

    :returns: NetlifyAccount
    """
    try:
        new_account = Account(
            id=account.id,
            full_name=account.user_metadata.full_name,
            avatar_url=account.user_metadata.avatar_url,
            email=account.email,
            role=account.role,
            provider=account.app_metadata.provider,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(new_account)
        db.commit()
        LOGGER.success(f"New Netlify account created: `{account.user_metadata.full_name}`")
        return account
    except IntegrityError as e:
        LOGGER.error(f"DB IntegrityError while creating Netlify user account: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while creating Netlify user account: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while creating Netlify user account: {e}")
