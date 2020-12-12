from mixpanel import Mixpanel

from config import settings
from database.schemas import NetlifyUser


def create_mixpanel_record(user: NetlifyUser):
    """
    Add user record to Mixpanel.

    :param user: New user account from Netlify auth.
    :type user: NetlifyUser
    """
    mp = Mixpanel(settings.MIXPANEL_API_TOKEN)
    body = {"$name": user.name, "$email": user.email}
    return mp.people_set(user.email, body)
