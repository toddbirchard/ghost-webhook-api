"""Creates missing image formats in a Google Cloud CDN."""
import requests
from io import BytesIO
from PIL import Image
from api import gcs
from google.cloud import storage
from api.log import logger


class ImageTransformer:

    def __init__(self, bucket_name, bucket_url):
        self.bucket_name = bucket_name
        self.bucket_url = bucket_url
        self.num_images_checked = 0
        self.images_total = 0
        self.retina_images_transformed = []
        self.standard_images_transformed = []
        self.webp_images_transformed = []

    def bulk_transform_images(self, **kwargs):
        """Queue image transformation jobs."""
        for key, value in kwargs.items():
            self.images_total += len(value)
        if kwargs.get('retina_from_standard'):
            self.retina_transform(kwargs.get('retina_from_standard'))
        if kwargs.get('standard_from_retina'):
            self.standard_transform(kwargs.get('standard_from_retina'))
        if kwargs.get('webp_from_standard'):
            self.webp_transform(kwargs.get('webp_from_standard'))
        return {
            'retina': len(self.retina_images_transformed),
            'standard': len(self.standard_images_transformed),
            'webp': len(self.webp_images_transformed),
            'total': len(self.webp_images_transformed)
        }

    def transform_single_image(self, image_url):
        image_path = image_url.replace(self.bucket_url, '')
        image_blob = storage.Blob(image_path, gcs.bucket)
        dot_position = image_blob.name.rfind('.')
        new_image_name = image_blob.name[:dot_position] + '@2x' + image_blob.name[dot_position:]
        self._create_retina_image(image_blob, new_image_name)
        return f'Successfully created {new_image_name}.'

    def retina_transform(self, standard_images):
        """Find images missing a retina-quality counterpart."""
        for image_blob in standard_images:
            self.num_images_checked += 1
            logger.info(f'{self.num_images_checked} of {self.images_total} ({image_blob.name})')
            dot_position = image_blob.name.rfind('.')
            new_image_name = image_blob.name[:dot_position] + '@2x' + image_blob.name[dot_position:]
            existing_image_file = self._fetch_image_via_http(new_image_name)
            if existing_image_file is None:
                self._create_retina_image(image_blob, new_image_name)
        return self.retina_images_transformed

    def standard_transform(self, retina_images):
        """Find images missing a standard-res counterpart."""
        for image_blob in retina_images:
            self.num_images_checked += 1
            logger.info(f'{self.num_images_checked} of {self.images_total} ({image_blob.name})')
            if '@2x' in image_blob.name:
                standard_image_name = image_blob.name.replace('@2x', '')
                standard_image = self._fetch_image_via_http(standard_image_name)
                if standard_image is not None:
                    new_blob = gcs.bucket.copy_blob(image_blob, gcs.bucket, standard_image_name)
                    self.standard_images_transformed.append(new_blob.name)
        return self.standard_images_transformed

    def webp_transform(self, retina_images):
        """Find images missing a webp counterpart."""
        for image_blob in retina_images:
            self.num_images_checked += 1
            logger.info(f'{self.num_images_checked} of {self.images_total} ({image_blob.name})')
            new_image_name = image_blob.name.split('.')[0] + '.webp'
            image_file = self._fetch_image_via_http(new_image_name)
            if image_file is not None:
                new_blob = gcs.bucket.copy_blob(image_blob, gcs.bucket, new_image_name)
                self.webp_images_transformed.append(new_blob.name)
        return self.webp_images_transformed

    def _create_retina_image(self, image_blob, new_image_name):
        """Create retina versions of standard-res images."""
        original_image = self._fetch_image_via_http(image_blob.name)
        im = Image.open(BytesIO(original_image))
        width, height = im.size
        if width > 1000:
            new_blob = gcs.bucket.copy_blob(image_blob, gcs.bucket, new_image_name)
            self.retina_images_transformed.append(new_blob.name)

    def _fetch_image_via_http(self, url):
        """Determine if image exists via HTTP request."""
        image_request = requests.get(self.bucket_url + url)
        if image_request.headers['Content-Type'] in ('application/octet-stream', 'image/jpeg'):
            return image_request.content
        return None
