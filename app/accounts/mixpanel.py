"""New user analytics."""
from typing import Optional

from mixpanel import Mixpanel

from config import settings
from database.schemas import NetlifyAccount


def create_mixpanel_record(user: NetlifyAccount) -> Optional[dict]:
    """
    Add user record to Mixpanel.

    :param user: New user account from Netlify auth.
    :type user: NetlifyAccount
    """
    mp = Mixpanel(settings.MIXPANEL_API_TOKEN)
    body = {"$name": user.name, "$email": user.email}
    return mp.people_set(user.email, body)
