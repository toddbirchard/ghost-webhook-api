from mixpanel import Mixpanel
from config import Settings


def create_mixpanel_record(user):
    mp = Mixpanel(Settings().MIXPANEL_API_TOKEN)
    body = {"$name": user.name, "$email": user.email}
    return mp.people_set(user.email, body)
