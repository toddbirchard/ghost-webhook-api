import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr,
           colorize=True,
           level="INFO",
           format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
                  + "<light-green>{level}</light-green>: "
                  + "<light-white>{message}</light-white>"
           )
logger.add('logs/errors.log',
           colorize=True,
           level="ERROR",
           rotation="500 MB",
           format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
                  + "<light-red>{level}</light-red>: "
                  + "<light-white>{message}</light-white>"
           )
