"""Custom logger."""
from sys import stdout
from loguru import logger
from config import Config


def create_logger():
    """Create custom logger."""
    logger.remove()
    if Config.FLASK_ENV == 'production':
        logger.add(
            'logs/info.log',
            colorize=True,
            level="INFO",
            rotation="500 MB",
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
            + "<light-green>{level}</light-green>: "
            + "<light-white>{message}</light-white>"
        )
        logger.add(
            'logs/errors.log',
            colorize=True,
            level="ERROR",
            rotation="500 MB",
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
            + "<light-red>{level}</light-red>: "
            + "<light-white>{message}</light-white>"
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
