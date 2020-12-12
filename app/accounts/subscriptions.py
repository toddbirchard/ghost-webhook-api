from typing import Tuple

from clients import ghost
from clients.log import LOGGER
from database.schemas import NetlifyUser


def new_ghost_subscription(user: NetlifyUser) -> Tuple[str, int]:
    """
    Create Ghost member from Netlify identity signup.

    :param user: New user account from Netlify auth.
    :type user: NetlifyUser

    :returns: Tuple[str, int]
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
    else:
        error_type = response["errors"][0]["type"]
        if error_type == "ValidationError":
            LOGGER.info(
                f"Skipped Ghost member creation for existing user: {user.name} <{user.email}>"
            )
    return response, code
