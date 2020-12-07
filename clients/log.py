"""Custom logger."""
from sys import stdout

import simplejson as json
from loguru import logger

from config import Settings


def formatter(record):
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


def create_logger() -> logger:
    """Create custom logger."""
    logger.remove()
    logger.add(
        stdout,
        colorize=True,
        catch=True,
        format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
        + "<light-green>{level}</light-green>: "
        + "<light-white>{message}</light-white>",
    )
    # Readable logs
    logger.add(
        "logs/info.log",
        colorize=True,
        catch=True,
        format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
        + "<light-green>{level}</light-green>: "
        + "<light-white>{message}</light-white>",
    )
    logger.add("logs/info.json", format=formatter, rotation="500 MB", compression="zip")
    if Settings().ENVIRONMENT == "production":
        # Datadog
        logger.add(
            "logs/info.json", format=formatter, rotation="500 MB", compression="zip"
        )
    return logger


LOGGER = create_logger()
