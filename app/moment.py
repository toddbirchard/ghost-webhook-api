"""Get current EST time/date."""
from datetime import datetime, timedelta

import pytz


def get_current_time() -> str:
    """Get current UTC time."""
    now = datetime.now()
    return f'{now.strftime("%Y-%m-%dT%H:%M:%S")}.000Z'


def get_start_date_range(timeframe: int) -> str:
    """Get current date."""
    now = datetime.now(pytz.timezone("America/New_York"))
    start_date = now - timedelta(days=timeframe)
    return start_date.strftime("%Y-%m-%d")


def get_current_datetime() -> datetime:
    """Get current UTC datetime."""
    return datetime.now()
