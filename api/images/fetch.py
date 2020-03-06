"""Fetch images in a Google Cloud storage bucket CDN."""
from flask import current_app as api


def fetch(bucket, bucket_image_folder_prefixes):
    """Fetch all images from GCP bucket."""
    clean_unwanted_images(bucket, bucket_image_folder_prefixes)
    retina_images = fetch_retina_images(bucket, bucket_image_folder_prefixes)
    standard_images = fetch_standard_images(bucket, bucket_image_folder_prefixes)
    api.logger.info(f'Checking {len(retina_images)} retina and \
                {len(standard_images)} standard images \
                in {bucket_image_folder_prefixes}')
    return retina_images, standard_images


def fetch_standard_images(bucket, bucket_image_folder_prefixes):
    """List all standard-res images in bucket."""
    images = []
    for prefix in bucket_image_folder_prefixes:
        files = bucket.list_blobs(prefix=prefix)
        file_list = [file for file in files if '@2x' not in file.name and '.jpg' in file.name]
        images.extend(file_list)
    return images


def fetch_retina_images(bucket, bucket_image_folder_prefixes):
    """List all retina images in bucket."""
    images = []
    for prefix in bucket_image_folder_prefixes:
        files = bucket.list_blobs(prefix=prefix)
        file_list = [file for file in files if '@2x' in file.name and 'webp' not in file.name]
        images.extend(file_list)
    return images


def clean_unwanted_images(bucket, bucket_image_folder_prefixes):
    """Remove unused images."""
    retina_images = fetch_retina_images(bucket, bucket_image_folder_prefixes)
    standard_images = fetch_standard_images(bucket, bucket_image_folder_prefixes)
    for image_blob in retina_images:
        if '@2x@2x' in image_blob.name or '_o@' in image_blob.name:
            bucket.delete_blob(image_blob.name)
            api.logger.info(f'deleted {image_blob.name}')
    for image_blob in standard_images:
        if '_o.' in image_blob.name:
            bucket.delete_blob(image_blob.name)
            api.logger.info(f'deleted {image_blob.name}')
