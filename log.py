"""Custom logger."""
from sys import stdout

import simplejson as json
from loguru import logger

from config import basedir, settings

DD_APM_FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s "
    "dd.version=%(dd.version)s "
    "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s]"
    "- %(message)s"
)


def json_formatter(record):
    """Pass raw log to be serialized."""

    def serialize(log):
        """Parse log message into Datadog JSON format."""
        subset = {
            "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
            "message": log["message"],
            "level": log["level"].name,
            "function": log.get("function"),
            "module": log.get("name"),
        }
        if log.get("exception", None):
            subset.update({"exception": log["exception"]})
        return json.dumps(subset)

    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]},\n"


def log_formatter(record: dict) -> str:
    """
    Formatter for .log records

    :param record: Log object containing log metadata & message.
    :type record: dict
    :returns: str
    """
    if record["level"].name == "TRACE":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #cfe2f3>{level}</fg #cfe2f3>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "INFO":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "WARNING":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> |  <fg #b09057>{level}</fg #b09057>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "SUCCESS":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #6dac77>{level}</fg #6dac77>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "ERROR":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #a35252>{level}</fg #a35252>: <light-white>{message}</light-white>\n"
    return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"


def create_logger() -> logger:
    """Create custom logger."""
    logger.remove()
    logger.add(
        stdout,
        colorize=True,
        catch=True,
        format=log_formatter,
    )
    # Readable logs
    if settings.ENVIRONMENT == "production":
        # Datadog
        logger.add(
            "/var/log/api/info.json",
            format=json_formatter,
            rotation="500 MB",
            compression="zip",
        )
        logger.add(
            "/var/log/api/apm.log",
            format=DD_APM_FORMAT,
            rotation="500 MB",
            compression="zip",
        )
        logger.add(
            f"/var/log/api/info.log",
            colorize=True,
            catch=True,
            format=log_formatter,
            rotation="500 MB",
            compression="zip",
        )
    else:
        logger.add(
            f"{basedir}/logs/error.log",
            colorize=True,
            catch=True,
            format=log_formatter,
            rotation="500 MB",
            compression="zip",
            level="ERROR",
        )
    return logger


# Custom logger
LOGGER = create_logger()
