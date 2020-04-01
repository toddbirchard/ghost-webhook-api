"""Fetch images from a Google Cloud Storage bucket."""
from flask import current_app as api
from random import randint
from api import gcs


def fetch_recent_images(prefixes):
    """Fetch all images from GCP bucket."""
    retina_images = fetch_retina_images(prefixes)
    standard_images = fetch_standard_images(prefixes)
    api.logger.info(f'Checking {len(retina_images)} retina and \
                {len(standard_images)} standard images \
                in {prefixes}')
    return retina_images, standard_images


def fetch_standard_images(prefixes):
    """List all standard-res images in bucket."""
    images = []
    for prefix in prefixes:
        files = gcs.bucket.list_blobs(prefix=prefix)
        file_list = [file for file in files if '@2x' not in file.name and '.jpg' in file.name]
        images.extend(file_list)
    return images


def fetch_retina_images(prefixes):
    """List all retina images in bucket."""
    images = []
    for prefix in prefixes:
        files = gcs.bucket.list_blobs(prefix=prefix)
        file_list = [file for file in files if '@2x' in file.name and 'webp' not in file.name]
        images.extend(file_list)
    return images


def fetch_random_image():
    """Fetch random Lynx image from GCS."""
    lynx_images = gcs.bucket.list_blobs(prefix='lynx/')
    images = [f"{api.config['GCP_BUCKET_URL']}{image.name}" for image in lynx_images if '@2x.jpg' in image.name]
    rand = randint(0, len(images) - 1)
    image = images[rand]
    return image
