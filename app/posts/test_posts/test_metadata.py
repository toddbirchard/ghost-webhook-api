from app.posts import batch_insert_metadata
from clients.log import LOGGER


def test_batch_insert_metadata():
    posts = batch_insert_metadata()
    LOGGER.info(posts)
