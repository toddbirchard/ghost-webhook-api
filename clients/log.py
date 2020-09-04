"""Custom logger."""
import simplejson as json
from sys import stdout
from loguru import logger
from config import Config


def serialize(record):
    subset = {"time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"), "message": record["message"]}
    return json.dumps(subset)


def formatter(record):
    # Note this function returns the string to be formatted, not the actual message to be logged
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]},\n"


def create_logger() -> logger:
    """Create custom logger."""
    logger.remove()
    if Config.FLASK_ENV == 'production':
        logger.add(
            'logs/info.log',
            colorize=True,
            level="INFO",
            rotation="200 MB",
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
                   + "<light-green>{level}</light-green>: "
                   + "<light-white>{message}</light-white>"
        )
        logger.add(
            'logs/errors.log',
            colorize=True,
            level="ERROR",
            rotation="200 MB",
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
                   + "<light-red>{level}</light-red>: "
                   + "<light-white>{message}</light-white>"
        )
        logger.add(
            'logs/info.json',
            format=formatter,
            level="INFO",
        )
        logger.add(
            'logs/errors.json',
            format=formatter,
            level="ERROR",
        )
    else:
        # Output logs to console while in development
        logger.add(
            stdout,
            colorize=True,
            level="INFO",
            catch=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
            + "<light-green>{level}</light-green>: "
            + "<light-white>{message}</light-white>"
        )
    return logger


LOGGER = create_logger()
