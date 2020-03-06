from flask import current_app as api
from random import randint
from api import gcs


def get_random_image():
    """Fetch random Lynx image from GCS."""
    lynx_images = gcs.list_blobs(prefix='lynx/')
    images = [f"{api.config['GCP_BUCKET_URL']}{image.name}" for image in lynx_images if '@2x.jpg' in image.name]
    rand = randint(0, len(images) - 1)
    image = images[rand]
    return image
