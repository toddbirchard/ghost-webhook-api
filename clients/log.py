"""Custom logger."""
from sys import stdout
import simplejson as json
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
    if Config.FLASK_ENV == 'production':
        logger.add(
            'logs/info.log',
            colorize=True,
            level="INFO",
            rotation="200 MB",
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> <light-green>{level}</light-green>:<light-white>{message}</light-white>"
        )
        logger.add(
            'logs/errors.log',
            colorize=True,
            level="ERROR",
            rotation="200 MB",
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> <light-red>{level}</light-red>:<light-white>{message}</light-white>"
        )
        # Datadog
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
        # APM
        apm_format = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
                      '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
                      '- %(message)s')
        logger.add(
            'logs/apm.json',
            format=apm_format,
            level="INFO",
        )
    return logger


LOGGER = create_logger()
