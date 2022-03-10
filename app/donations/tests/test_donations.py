"""
import pytest
from fastapi import Depends
from sqlalchemy.orm import Session

from database.orm import get_db
from database.schemas import NewDonation
from database.crud import get_donation


@pytest.fixture
def old_donation() -> NewDonation:
    return NewDonation(
        name="todd",
        email="fakeemail@example.com",
        count=1,
        message="This is a fake comment.",
        link="https://www.buymeacoffee.com/hackersslackers/c/12345",
        coffee_id=12345,
    )


def test_get_donation(old_donation: NewDonation, db: Session = Depends(get_db)):
    donation = get_donation(db, old_donation)
    assert donation is not None
"""
