"""Create missing image formats in a Google Cloud CDN."""
from random import randint
from io import BytesIO
import requests
from PIL import Image
from google.cloud import storage
from api.log import LOGGER


class ImageTransformer:
    """Transform post feature images."""

    def __init__(self, google_cloud_storage):
        self.gcs = google_cloud_storage
        self.num_images_checked = 0
        self.images_total = 0

    def fetch_image_blobs(self, folder, image_type=None):
        """Retrieve images from GCS bucket matching directory & filter conditions."""
        files = self.gcs.client.list_blobs(prefix=folder)
        image_filter = {
            'remove': None,
            'require': None
        }
        if image_type == 'retina':
            image_filter['remove'] = '@2x'
            image_filter['require'] = '.jpg'
        elif image_type == 'standard':
            image_filter['remove'] = '.webp'
            image_filter['require'] = '@2x'
        else:
            return files
        file_list = [file for file in files if image_filter['remove'] in file.name and image_filter['require'] not in file.name]
        return file_list

    def bulk_transform_images(self, folder, standard_images, retina_images):
        """Image transformation jobs."""
        self.num_images_checked = 0
        self.images_total = len(standard_images) + len(retina_images)
        self._purge_unwanted_images(folder)
        retina_transformed = self.retina_transformations(standard_images)
        standard_transformed = self.standard_transformations(retina_images)
        webp_transformed = self.webp_transformations(retina_images)
        return retina_transformed, standard_transformed, webp_transformed

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

    def retina_transformations(self, standard_images):
        """Find images missing a retina-quality counterpart."""
        LOGGER.info('Step 2: Generating retina images...')
        images_transformed = 0
        for image_blob in standard_images:
            self.num_images_checked += 1
            LOGGER.info(f"Checking {self.num_images_checked} of {self.images_total} retina transformations.")
            dot_position = image_blob.name.rfind('.')
            new_image_name = image_blob.name[:dot_position] + '@2x' + image_blob.name[dot_position:]
            existing_image_file = self._fetch_image_via_http(new_image_name)
            if existing_image_file is None:
                LOGGER.info(f'Creating retina image {new_image_name}')
                self._create_retina_image(image_blob, new_image_name)
                images_transformed += 1
        return images_transformed

    def standard_transformations(self, retina_images):
        """Find images missing a standard-res counterpart."""
        LOGGER.info('Step 3: Generating standard resolution images...')
        images_transformed = 0
        for image_blob in retina_images:
            self.num_images_checked += 1
            LOGGER.info(f"Checking {self.num_images_checked} of {self.images_total} standard transformations.")
            if '@2x' in image_blob.name:
                standard_image_name = image_blob.name.replace('@2x', '')
                standard_image = self._fetch_image_via_http(standard_image_name)
                if standard_image is not None:
                    LOGGER.info(f'Creating standard image {standard_image_name}')
                    self.gcs.bucket.copy_blob(image_blob, self.gcs.bucket, standard_image_name)
                    images_transformed += 1
        return images_transformed

    def webp_transformations(self, retina_images):
        """Find images missing a webp counterpart."""
        LOGGER.info('Step 4: Generating webp images...')
        images_transformed = 0
        for image_blob in retina_images:
            self.num_images_checked += 1
            LOGGER.info(f"Checking {self.num_images_checked} of {self.images_total} webp transformations.")
            new_image_name = image_blob.name.split('.')[0] + '.webp'
            image_file = self._fetch_image_via_http(new_image_name)
            if image_file is not None:
                LOGGER.info(f'Creating webp image {new_image_name}')
                self.gcs.bucket.copy_blob(image_blob, self.gcs.bucket, new_image_name)
                images_transformed += 1
        return images_transformed

    @LOGGER.catch
    def create_single_retina_image(self, image_url):
        """Create retina version of single image."""
        image_path = image_url.replace(self.gcs.bucket_url, '')
        image_blob = storage.Blob(image_path, self.gcs.bucket)
        dot_position = image_blob.name.rfind('.')
        new_image_name = image_blob.name[:dot_position] + '@2x' + image_blob.name[dot_position:]
        existing_image_file = self._fetch_image_via_http(new_image_name)
        if existing_image_file is None:
            LOGGER.info(f'Creating retina image {new_image_name}')
            self._create_retina_image(image_blob, new_image_name)
        return f'{self.gcs.bucket_http_url}{new_image_name}'

    def fetch_random_lynx_image(self):
        """Fetch random Lynx image from GCS bucket."""
        lynx_images = self.gcs.client.list_blobs(prefix='roundup')
        images = [f"{self.gcs.bucket_http_url}{image.name}" for image in lynx_images if '@2x.jpg' in image.name]
        rand = randint(0, len(images) - 1)
        image = images[rand]
        LOGGER.info(f'Selected random Lynx image {image}')
        return image

    @LOGGER.catch
    def _create_retina_image(self, image_blob, new_image_name):
        """Create retina versions of standard-res images."""
        original_image = self._fetch_image_via_http(new_image_name)
        if original_image:
            img = Image.open(BytesIO(original_image))
            width, height = img.size
            if width > 1000:
                self.gcs.bucket.copy_blob(image_blob, self.gcs.bucket, new_image_name)

    @LOGGER.catch
    def _fetch_image_via_http(self, new_image_name):
        """Determine if image exists via HTTP request."""
        LOGGER.info(f'Checking {self.gcs.bucket_http_url}{new_image_name}')
        image_request = requests.get(self.gcs.bucket_http_url, new_image_name)
        if image_request.headers['Content-Type'] in ('application/octet-stream', 'image/jpeg'):
            return image_request.content
        return None
