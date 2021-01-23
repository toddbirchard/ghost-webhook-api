from datetime import datetime

from sqlalchemy.engine.result import ResultProxy
from sqlalchemy.orm import Session

from clients.log import LOGGER
from database.models import Comment, Donation
from database.schemas import NewComment, NewDonation


def get_donation(db: Session, donation_id: int) -> ResultProxy:
    """
    Fetch BuyMeACoffee donation by ID.

    :param db: ORM database session.
    :type db: Session
    :param donation_id: Primary key for donation record.
    :type donation_id: int
    :returns: ResultProxy
    """
    return db.query(Donation).filter(Donation.coffee_id == donation_id).first()


def create_donation(db: Session, donation: NewDonation) -> Donation:
    """
    Create new BuyMeACoffee donation record.

    :param db: ORM database session.
    :type db: Session
    :param donation: Donation schema object.
    :type donation: NewDonation
    :returns: Donation
    """
    db_item = Donation(
        email=donation.email,
        name=donation.name,
        count=donation.count,
        message=donation.message,
        link=donation.link,
        coffee_id=donation.coffee_id,
        created_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    return db_item


def get_comment(db: Session, comment_id: int) -> ResultProxy:
    """
    Fetch BuyMeACoffee donation by ID.

    :param db: ORM database session.
    :type db: Session
    :param comment_id: Primary key for user comment record.
    :type comment_id: int
    :returns: ResultProxy
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


def create_comment(db: Session, comment: NewComment):
    """
    Create new BuyMeACoffee donation record.

    :param db: ORM database session.
    :type db: Session
    :param comment: User comment schema object.
    :type comment: NewComment
    :returns: Comment
    """
    new_comment = Comment(
        user_name=comment.user_name,
        user_avatar=comment.user_avatar,
        user_id=comment.user_id,
        user_email=comment.user_email,
        body=comment.body,
        created_at=datetime.now(),
        post_slug=comment.post_slug,
        post_id=comment.post_id,
    )
    db.add(new_comment)
    db.commit()
    LOGGER.success(
        f"New comment submitted by user `{new_comment.user_name}` on post `{new_comment.post_slug}`"
    )
    return new_comment
