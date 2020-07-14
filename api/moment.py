"""Get current EST time."""
import pytz
from datetime import datetime, timedelta


def get_current_time(updated_at):
	"""Get current EST time"""
	updated_time = updated_at.replace('z', '')
	updated_time = datetime.strptime(updated_time, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(seconds=1, hours=1)
	return updated_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ").replace(' ', '')