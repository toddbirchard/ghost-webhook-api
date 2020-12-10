from app.posts.img_tags import find_images
from clients.log import LOGGER


def test_find_images():
    images = find_images()
    LOGGER.info(images)
