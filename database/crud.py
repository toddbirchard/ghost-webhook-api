from datetime import datetime
from typing import List, Optional

from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database.models import Account, Donation, TrendingPostInsight
from database.schemas import NetlifyAccount, NewDonation, PostInsight
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


def create_donation(db: Session, donation: NewDonation) -> Donation:
    """
    Create new BuyMeACoffee donation record.

    :param Session db: ORM database session.
    :param NewDonation donation: Donation schema object.

    :returns: Donation
    """
    try:
        donation_record = Donation(
            coffee_id=donation.coffee_id,
            email=donation.email,
            name=donation.name,
            count=donation.count,
            message=donation.message,
            link=donation.link,
            created_at=datetime.now(),
        )
        db.add(donation_record)
        db.commit()
        LOGGER.success(f"Successfully received donation: `{donation.count}` coffees from `{donation.name}`.")
        return donation_record
    except IntegrityError as e:
        LOGGER.error(f"DB IntegrityError while persisting donation: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while persisting donation: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while persisting donation: {e}")


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
        LOGGER.success(f"Successfully created new Netlify account created: `{account.user_metadata.full_name}`")
        return account
    except IntegrityError as e:
        LOGGER.error(f"DB IntegrityError while persisting Netlify user: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while persisting Netlify user: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while persisting Netlify user: {e}")


def update_trending_insights(db: Session, trending_post_insights: List[PostInsight]) -> List[TrendingPostInsight]:
    """
    Refresh `trending_post_insight` table with fresh results from previous 14 days.
    This is a destructive action that will purge and replace all "trending post" records.

    :param Session db: ORM database session.
    :param List[PostInsight] trending_post_insights: Collection of top-visited URLs from Plausible.

    :returns: List[TrendingPostInsight]
    """
    try:
        table_name = trending_post_insights[0].__tablename__()
        db.execute(f"TRUNCATE TABLE {table_name};")
        db.add_all(trending_post_insights)
        db.commit()
        LOGGER.success(f"Successfully bulk-updated {len(trending_post_insights)} `TrendingPostInsight` records.")
        return db.query(TrendingPostInsight).all()
    except IntegrityError as e:
        LOGGER.error(f"DB IntegrityError while batch persisting TrendingPostInsight: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while batch persisting TrendingPostInsight: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while batch persisting TrendingPostInsight: {e}")
