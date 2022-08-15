"""Mixpanel user analytics."""
from typing import Optional

from mixpanel import Mixpanel, MixpanelException

from config import settings
from database.schemas import GhostMember
from log import LOGGER


def create_mixpanel_record(user: GhostMember) -> Optional[dict]:
    """
    Add user record to Mixpanel.

    :param Member user: New user account from Netlify auth.

    :returns: Optional[dict]
    """
    try:
        mp = Mixpanel(settings.MIXPANEL_API_TOKEN)
        body = {"$name": user.name, "$email": user.email}
        new_user = mp.people_set(user.email, body)
        if new_user:
            return new_user
        return None
    except MixpanelException as e:
        LOGGER.warning(f"Mixpanel failed to register user: {e}")
    except Exception as e:
        LOGGER.warning(f"Unexpected failure when registering Mixpanel user: {e}")
