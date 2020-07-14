"""Get current EST time."""
import pytz
from datetime import datetime


def get_current_time():
	"""Get current EST time"""
	return datetime.now(tz=pytz.timezone('America/New_York')).strftime("%Y-%m-%dT%H:%M:%S.000Z").replace(' ', '')
