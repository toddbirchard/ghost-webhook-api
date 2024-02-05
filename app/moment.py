"""Calculate situational time or dates."""

from datetime import datetime, timedelta

import pytz


def get_current_time() -> str:
    """
    Get current UTC time as formatted string.

    :returns: str
    """
    now = datetime.now()
    return f'{now.strftime("%Y-%m-%dT%H:%M:%S")}.000Z'


def get_start_date_range(duration: int) -> str:
    """
    Calculate start date of a date range, given a number of days.

    :param int duration: Number of days to calculate a date range for.

    :returns: str
    """
    now = datetime.now(pytz.timezone("America/New_York"))
    start_date = now - timedelta(days=duration)
    return start_date.strftime("%Y-%m-%d")


def get_current_datetime() -> datetime:
    """
    Get current UTC datetime.

    :returns: datetime
    """
    return datetime.now()
