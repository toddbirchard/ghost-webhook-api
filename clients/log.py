"""Custom logger."""
from sys import stdout
from loguru import logger
from config import Config
import json_log_formatter



def create_logger() -> logger:
    """Create custom logger."""
    formatter = json_log_formatter.JSONFormatter()
    logger.remove()
    if Config.FLASK_ENV == 'production':
        logger.add(
            'logs/info.json',
            level="INFO",
            rotation="200 MB",
            serialize=True
        )
        logger.add(
            'logs/errors.json',
            level="ERROR",
            rotation="200 MB",
            serialize=True
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
