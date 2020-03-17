"""Purge unwanted images from CDN."""
from flask import current_app as api
from api import gcs


def clean_unwanted_images(retina_images, standard_images):
    """Remove unused images."""
    for image_blob in retina_images:
        if '@2x@2x' in image_blob.name or '_o@' in image_blob.name:
            gcs.bucket.delete_blob(image_blob.name)
            api.logger.info(f'deleted {image_blob.name}')
    for image_blob in standard_images:
        if '_o.' in image_blob.name:
            gcs.bucket.delete_blob(image_blob.name)
            api.logger.info(f'deleted {image_blob.name}')
