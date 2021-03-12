"""New user analytics."""
from typing import Optional

from mixpanel import Mixpanel, MixpanelException

from clients.log import LOGGER
from config import settings
from database.schemas import Member


def create_mixpanel_record(user: Member) -> Optional[dict]:
    """
    Add user record to Mixpanel.

    :param user: New user account from Netlify auth.
    :type user: NetlifyAccount
    """
    try:
        mp = Mixpanel(settings.MIXPANEL_API_TOKEN)
        body = {"$name": user.name, "$email": user.email}
        return mp.people_set(user.email, body)
    except MixpanelException as e:
        LOGGER.warning(f"Mixpanel failed to register user: {e}")
    except Exception as e:
        LOGGER.warning(f"Unexpected failure when registering Mixpanel user: {e}")
