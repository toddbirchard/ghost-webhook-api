"""Get current EST time/date."""
import pytz
from datetime import datetime, timedelta


def get_current_time() -> str:
    """Get current UTC time."""
    now = datetime.now(pytz.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f")


def get_current_date(timeframe: int) -> str:
    """Get current date."""
    now = datetime.now(pytz.utc)
    start_date = now - timedelta(days=timeframe)
    return start_date.strftime("%Y-%m-%d")


def get_current_datetime() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(pytz.utc)
