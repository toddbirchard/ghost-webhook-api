"""Ghost subscription creation."""
from typing import Dict, List, Optional

from clients import ghost
from database.schemas import NetlifyAccount
from log import LOGGER


def new_ghost_subscription(user: NetlifyAccount) -> Optional[Dict[str, List[Dict]]]:
    """
    Create Ghost member from Netlify identity signup.

    :param NetlifyAccount user: New user account from Netlify auth.

    :returns: Optional[str, Dict[List[Dict]]]
    """
    body = {
        "accounts": [
            {
                "name": user.user_metadata.full_name,
                "email": user.email,
                "note": "Subscribed from Netlify",
                "subscribed": True,
                "comped": False,
                "labels": user.user_metadata.roles,
            }
        ]
    }
    response, code = ghost.create_member(body)
    if code == 200:
        LOGGER.success(
            f"Created new Ghost member: {user.user_metadata.full_name} <{user.email}>"
        )
        return body
    else:
        error_type = response["errors"][0]["type"]
        if error_type == "ValidationError":
            LOGGER.info(
                f"Skipped Ghost member creation for existing user: {user.user_metadata.full_name} <{user.email}>"
            )
