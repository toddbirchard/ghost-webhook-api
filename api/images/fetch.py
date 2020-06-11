"""Fetch images from a Google Cloud Storage bucket."""
from flask import current_app as api
from random import randint
from api import gcs
from api.log import LOGGER


def fetch_image_blobs(prefixes):
    """List all images from GCS bucket."""
    retina_images = fetch_retina_images(prefixes)
    standard_images = fetch_standard_images(prefixes)
    LOGGER.info(f'Checking {len(retina_images)} retina and \
                {len(standard_images)} standard images \
                in {prefixes}')
    return retina_images, standard_images


def fetch_standard_images(prefixes):
    """List all standard resolution images in GCS bucket."""
    images = []
    for prefix in prefixes:
        files = gcs.bucket.list_blobs(prefix=prefix)
        file_list = [file for file in files if '@2x' not in file.name and '.jpg' in file.name]
        images.extend(file_list)
    return images


def fetch_retina_images(prefixes):
    """List all retina images in GCS bucket."""
    images = []
    for prefix in prefixes:
        files = gcs.bucket.list_blobs(prefix=prefix)
        file_list = [file for file in files if '@2x' in file.name and 'webp' not in file.name]
        images.extend(file_list)
    return images


def fetch_random_lynx_image():
    """Fetch random Lynx image from GCS bucket."""
    lynx_images = gcs.bucket.list_blobs(prefix=f'{api.config["GCP_BUCKET_FOLDER"]}/')
    images = [f"{api.config['GCP_BUCKET_URL']}{image.name}" for image in lynx_images if '@2x.jpg' in image.name]
    rand = randint(0, len(images) - 1)
    image = images[rand]
    LOGGER.info(f'Selected random lynx image {image}')
    return image
