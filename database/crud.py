from datetime import datetime

from sqlalchemy.orm import Session

from .models import Comment, Donation
from .schemas import NewComment, NewDonation


def get_donation(db: Session, donation_id: int):
    return db.query(Donation).filter(Donation.coffee_id == donation_id).first()


def create_donation(db: Session, donation: NewDonation):
    db_item = Donation(
        email=donation.email,
        name=donation.name,
        count=donation.count,
        message=donation.message,
        link=donation.link,
        coffee_id=donation.coffee_id,
        created_at=datetime.strptime(donation.created_at, "%Y-%m-%d"),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_comment(db: Session, comment_id: str):
    return db.query(Comment).filter(Comment.comment_id == comment_id).first()


def create_comment(db: Session, comment: NewComment):
    db_item = Comment(
        comment_id=comment.comment_id,
        user_name=comment.user_name,
        user_avatar=comment.user_avatar,
        user_id=comment.user_id,
        user_email=comment.user_email,
        body=comment.body,
        created_at=datetime.now(),
        post_slug=comment.post_slug,
        author_name=comment.author_name,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
