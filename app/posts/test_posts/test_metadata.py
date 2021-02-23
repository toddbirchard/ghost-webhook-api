from app.posts import batch_update_metadata
from clients.log import LOGGER


def test_batch_insert_metadata():
    post_updates = batch_update_metadata()
    assert type(post_updates) == dict
    LOGGER.info(post_updates)
