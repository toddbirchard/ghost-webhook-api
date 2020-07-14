"""Get current EST time."""
import pytz
from datetime import datetime, timedelta


def get_current_time(updated_at):
	"""Get current EST time"""
	updated_time = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.000Z") + timedelta(seconds=1)
	return updated_time.strftime("%Y-%m-%dT%H:%M:%S.%z").replace(' ', '')