from typing import Tuple

from clients import ghost
from clients.log import LOGGER


def new_ghost_subscription(data: dict) -> Tuple[str, int]:
    """Create Ghost member from Netlify identity signup."""
    body = {
        "members": [
            {
                "name": data.get("name"),
                "email": data.get("email"),
                "note": data.get("ip_address"),
                "subscribed": True,
                "comped": False,
                "labels": [data.get("provider")],
            }
        ]
    }
    response, code = ghost.create_member(body)
    if code == 200:
        LOGGER.info(
            f"Created new Ghost member: {data.get('name')} <{data.get('email')}>"
        )
    else:
        error_type = response["errors"][0]["type"]
        if error_type == "ValidationError":
            LOGGER.info(
                f"Skipped Ghost member creation for existing user: {data.get('name')} <{data.get('email')}>"
            )
    return response, code
