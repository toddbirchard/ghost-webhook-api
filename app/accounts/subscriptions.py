"""Ghost subscription creation."""
from typing import Dict, List, Optional

from clients import ghost
from clients.log import LOGGER
from database.schemas import NetlifyAccount


def new_ghost_subscription(user: NetlifyAccount) -> Optional[Dict[str, List[Dict]]]:
    """
    Create Ghost member from Netlify identity signup.

    :param user: New user account from Netlify auth.
    :type user: NetlifyAccount
    :returns: Optional[str, Dict[List[Dict]]]
    """
    body = {
        "accounts": [
            {
                "name": user.name,
                "email": user.email,
                "note": user.note,
                "subscribed": True,
                "comped": False,
                "labels": user.labels,
            }
        ]
    }
    response, code = ghost.create_member(body)
    if code == 200:
        LOGGER.success(f"Created new Ghost member: {user.name} <{user.email}>")
        return body
    else:
        error_type = response["errors"][0]["type"]
        if error_type == "ValidationError":
            LOGGER.info(
                f"Skipped Ghost member creation for existing user: {user.name} <{user.email}>"
            )
