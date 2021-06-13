from app.posts.metadata import batch_assign_img_alt
from log import LOGGER


def test_find_images():
    images = batch_assign_img_alt()
    LOGGER.info(images)
