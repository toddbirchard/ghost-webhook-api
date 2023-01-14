from datetime import datetime
from typing import Optional

from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database.models import Account, Donation
from database.schemas import NetlifyAccount, NewDonation
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
