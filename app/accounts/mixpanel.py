from mixpanel import Mixpanel
from config import Settings
from .models import User


def create_mixpanel_record(user: User):
    """Add user record to Mixpanel."""
    mp = Mixpanel(Settings().MIXPANEL_API_TOKEN)
    body = {"$name": user.name, "$email": user.email}
    return mp.people_set(user.email, body)
