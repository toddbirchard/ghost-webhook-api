"""Accept and persist `BuyMeACoffee` donations."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from clients import ghost
from database.crud import create_donation, get_donation
from database.orm import get_db
from database.schemas import NewDonation
from log import LOGGER

router = APIRouter(prefix="/donation", tags=["donations"])


@router.post(
    "/",
    summary="New BuyMeACoffee donation",
    description="Save record of new donation to persistent ledger.",
    response_model=NewDonation,
)
async def accept_donation(donation: NewDonation, db: Session = Depends(get_db)):
    """
    Save BuyMeACoffee donation to database.

    :param NewDonation donation: New donation.
    :param Session db: ORM Database session.

    :returns: donation
    """
    existing_donation = get_donation(db, donation)
    if existing_donation:
        LOGGER.warning(
            f"Donation `{donation.coffee_id}` from `{donation.email}` already exists; skipping."
        )
        raise HTTPException(
            status_code=400,
            detail=f"Donation `{donation.coffee_id}` from `{donation.email}` already exists; skipping.",
        )
    new_donation = create_donation(db=db, donation=donation)
    if new_donation:
        ghost.rebuild_netlify_site()
    return donation
