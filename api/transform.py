"""Creates missing image formats in a Google Cloud CDN."""
from random import randint
import requests
from io import BytesIO
from PIL import Image
from google.cloud import storage
from api.log import LOGGER


class ImageTransformer:
    """Transform post feature images."""

    def __init__(self, google_cloud_storage):
        self.gcs = google_cloud_storage
        self.num_images_checked = 0
        self.images_total = 0
        self.retina_images_transformed = []
        self.standard_images_transformed = []
        self.webp_images_transformed = []

    def fetch_image_blobs(self, folder, image_type=None):
        files = self.gcs.bucket.list_blobs(prefix=folder)
        filter = {
            'remove': None,
            'require': None
        }
        if image_type == 'retina':
            filter['remove'] = '@2x'
            filter['require'] = '.jpg'
        elif image_type == 'standard':
            filter['remove'] = '.webp'
            filter['require'] = '@2x'
        else:
            return [file for file in files]
        file_list = [file for file in files if filter['remove'] in file.name and filter['require'] not in file.name]
        return file_list

    def bulk_transform_images(self, folder, images, transformation=None):
        """Image transformation jobs."""
        transformed = None
        self.images_total = images
        self._purge_unwanted_images(folder)
        if transformation == 'retina':
            transformed = self.retina_transformations(images)
        elif transformation == 'standard':
            transformed = self.standard_transformations(images)
        elif transformation == 'webp':
            transformed = self.webp_transformations(images)
        return len(transformed)

    def retina_transformations(self, standard_images):
        """Find images missing a retina-quality counterpart."""
        LOGGER.info('Step 2: Generating retina images...')
        for image_blob in standard_images:
            self.num_images_checked += 1
            LOGGER.info(f"{self.num_images_checked} of {self.images_total} ({image_blob.name}).")
            dot_position = image_blob.name.rfind('.')
            new_image_name = image_blob.name[:dot_position] + '@2x' + image_blob.name[dot_position:]
            existing_image_file = self._fetch_image_via_http(new_image_name)
            if existing_image_file is None:
                self._create_retina_image(image_blob, new_image_name)
        return self.retina_images_transformed

    def standard_transformations(self, retina_images):
        """Find images missing a standard-res counterpart."""
        LOGGER.info('Step 3: Generating standard resolution images...')
        for image_blob in retina_images:
            self.num_images_checked += 1
            LOGGER.info(f'{self.num_images_checked} of {self.images_total} ({image_blob.name})')
            if '@2x' in image_blob.name:
                standard_image_name = image_blob.name.replace('@2x', '')
                standard_image = self._fetch_image_via_http(standard_image_name)
                if standard_image is not None:
                    new_blob = self.gcs.bucket.copy_blob(image_blob, self.gcs.bucket, standard_image_name)
                    self.standard_images_transformed.append(new_blob.name)
        return self.standard_images_transformed

    def webp_transformations(self, retina_images):
        """Find images missing a webp counterpart."""
        LOGGER.info('Step 3: Generating webp images...')
        for image_blob in retina_images:
            self.num_images_checked += 1
            LOGGER.info(f'{self.num_images_checked} of {self.images_total} ({image_blob.name})')
            new_image_name = image_blob.name.split('.')[0] + '.webp'
            image_file = self._fetch_image_via_http(new_image_name)
            if image_file is not None:
                new_blob = self.gcs.bucket.copy_blob(image_blob, self.gcs.bucket, new_image_name)
                self.webp_images_transformed.append(new_blob.name)
        return self.webp_images_transformed

    @LOGGER.catch
    def transform_single_image(self, image_url):
        """Create retina version of single image."""
        image_path = image_url.replace(self.gcs.bucket_url, '')
        image_blob = storage.Blob(image_path, self.gcs.bucket)
        dot_position = image_blob.name.rfind('.')
        new_image_name = image_blob.name[:dot_position] + '@2x' + image_blob.name[dot_position:]
        self._create_retina_image(image_blob, new_image_name)
        return f'{self.gcs.bucket_http_url}{new_image_name}'

    def fetch_random_lynx_image(self):
        """Fetch random Lynx image from GCS bucket."""
        lynx_images = self.gcs.bucket.list_blobs(prefix='roundup')
        images = [f"{self.gcs.bucket_http_url }{image.name}" for image in lynx_images if '@2x.jpg' in image.name]
        rand = randint(0, len(images) - 1)
        image = images[rand]
        LOGGER.info(f'Selected random Lynx image {image}')
        return image

    @LOGGER.catch
    def _purge_unwanted_images(self, folder):
        """Delete images which have been compressed or generated multiple times."""
        LOGGER.info('Step 1: Purging unwanted images...')
        substrings = ['@2x@2x', '_o', 'psd', '?']
        image_blobs = self.gcs.get(folder)
        for image_blob in image_blobs:
            if any(substr in image_blob.name for substr in substrings):
                self.gcs.bucket.delete_blob(image_blob.name)
                LOGGER.info(f'Deleted {image_blob.name}.')
        return self.gcs.get(folder)

    @LOGGER.catch
    def _create_retina_image(self, image_blob, new_image_name):
        """Create retina versions of standard-res images."""
        original_image = self._fetch_image_via_http(new_image_name)
        if original_image:
            im = Image.open(BytesIO(original_image))
            width, height = im.size
            if width > 1000:
                new_blob = self.gcs.bucket.copy_blob(image_blob, self.gcs.bucket, new_image_name)
                self.retina_images_transformed.append(new_blob.name)

    @LOGGER.catch
    def _fetch_image_via_http(self, new_image_name):
        """Determine if image exists via HTTP request."""
        image_request = requests.get(self.gcs.bucket_http_url, new_image_name)
        if image_request.headers['Content-Type'] in ('application/octet-stream', 'image/jpeg'):
            return image_request.content
        return None
