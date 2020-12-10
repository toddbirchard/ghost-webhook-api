from app.posts.img_tags import assign_alt_text_to_imgs
from clients.log import LOGGER


def test_find_images():
    images = assign_alt_text_to_imgs()
    LOGGER.info(images)
