"""Parse Donation into JSON response."""
from database.models import Donation


def parse_donation_json(donation: Donation) -> dict:
    """
    Transform `donation` object to JSON.

    :param Donation donation: Ghost member subscribed to receive newsletters.

    :returns: dict
    """
    return {
        "id": donation.id,
        "coffee_id": donation.coffee_id,
        "email": donation.email,
        "name": donation.name,
        "count": donation.count,
        "message": donation.message,
        "link": donation.link,
        "created_at": donation.created_at,
    }
