"""Accept and persist `BuyMeACoffee` donations."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from clients import ghost
from database.crud import create_donation, get_donation
from database.orm import get_db
from database.schemas import NewDonation

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

    :param NewDonation donation: Incoming new donation.
    :param Session db: ORM Database session.

    :returns: donation
    """
    existing_donation = get_donation(db, donation)
    if existing_donation:
        raise HTTPException(
            status_code=400,
            detail=f"Donation `{donation.coffee_id}` from `{donation.email}` already exists; skipping.",
        )
    new_donation = create_donation(db, donation)
    if new_donation:
        ghost.rebuild_netlify_site()
    return donation


@router.delete(
    "/",
    summary="Delete BuyMeACoffee donation record",
    description="Delete BuyMeACoffee donation transaction by ID.",
    response_model=NewDonation,
)
async def delete_donation(donation: NewDonation, db: Session = Depends(get_db)):
    """
    Delete BuyMeACoffee donation from database.

    :param NewDonation donation: Incoming new donation.
    :param Session db: ORM Database session.

    :returns: donation
    """
    existing_donation = get_donation(db, donation)
    if existing_donation:
        raise HTTPException(
            status_code=400,
            detail=f"Donation `{donation.coffee_id}` from `{donation.email}` already exists; skipping.",
        )
    new_donation = create_donation(db, donation)
    if new_donation:
        ghost.rebuild_netlify_site()
    return donation
