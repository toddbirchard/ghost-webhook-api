"""Initialize celery with Flask."""
from celery import Celery
from config import Config
from api.log import LOGGER


celery = Celery(
	'tasks',
	backend=Config.CELERY_RESULT_BACKEND,
	broker=Config.CELERY_BROKER_URL,
	timezone='America/New_York',
	log=LOGGER,
)
