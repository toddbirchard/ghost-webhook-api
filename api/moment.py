"""Get current EST time."""
import pytz
from datetime import datetime


def get_current_time():
	"""Get current EST time"""
	now = datetime.now(pytz.utc)
	return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-6] + '000Z'
