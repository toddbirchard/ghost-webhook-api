"""Google Cloud Storage client and image transformer."""
from typing import List, Optional
import io
from math import floor
from google.cloud import storage
from google.cloud.storage.blob import Blob
from random import randint
from io import BytesIO
import requests
from PIL import Image
from clients.log import LOGGER


class GCS:
    """Google Cloud Storage CDN."""

    def __init__(
            self,
            bucket_name: str,
            bucket_url: str,
            bucket_lynx: str
    ):
        self.bucket_name = bucket_name
        self.bucket_url = bucket_url
        self.bucket_lynx = bucket_lynx

    @property
    def client(self):
        """Google Cloud Storage client."""
        return storage.Client()

    @property
    def bucket(self):
        """Google Cloud Storage bucket where memes are stored."""
        return self.client.get_bucket(self.bucket_name)

    @property
    def bucket_http_url(self):
        """Publicly accessible URL for images.."""
        return self.bucket_url

    def get(self, prefix: str):
        """
        Retrieve all blobs in a bucket containing a prefix.
        :param prefix: Substring to match against filenames.
        :type prefix: str
        """
        return self.bucket.list_blobs(prefix=prefix)

    def fetch_blobs(self, folder, image_type=None) -> List[Optional[Blob]]:
        """Retrieve images from GCS bucket matching directory & filter conditions."""
        files = self.get(prefix=folder)
        if image_type == 'retina':
            return [file for file in files if '@2x.jpg' in file.name and '_mobile' not in file.name]
        return [file for file in files if '@2x' not in file.name and '_mobile' not in file.name]

    @LOGGER.catch
    def purge_unwanted_images(self, folder):
        """Delete images which have been compressed or generated multiple times."""
        LOGGER.info('Purging unwanted images...')
        substrings = ['@2x@2x', '_o', 'psd', '?', '_mobile_mobile']
        image_blobs = self.get(folder)
        for image_blob in image_blobs:
            if any(substr in image_blob.name for substr in substrings):
                self.bucket.delete_blob(image_blob.name)
                LOGGER.info(f'Deleted {image_blob.name}.')
        return self.get(folder)

    def retina_transformations(self, folder) -> List[Optional[str]]:
        """Find images missing a retina-quality counterpart."""
        images_transformed = []
        LOGGER.info('Generating standard images...')
        for image_blob in self.fetch_blobs(folder):
            new_image_name = image_blob.name.replace('.jpg', '@2x.jpg')
            existing_image_file = self._fetch_image_via_http(new_image_name)
            if existing_image_file is None:
                LOGGER.info(f'Creating retina image {new_image_name}')
                self._create_retina_image(image_blob, new_image_name)
                images_transformed.append(new_image_name)
        return images_transformed

    def webp_transformations(self, folder) -> List[Optional[str]]:
        """Find images missing a webp counterpart."""
        images_transformed = []
        LOGGER.info('Generating webp images...')
        for image_blob in self.fetch_blobs(folder, image_type='retina'):
            new_image_name = image_blob.name.split('.')[0] + '.webp'
            image_file = self._fetch_image_via_http(new_image_name)
            if image_file is not None:
                LOGGER.info(f'Creating webp image {new_image_name}')
                self.bucket.copy_blob(image_blob, self.bucket, new_image_name)
                images_transformed.append(new_image_name)
        return images_transformed

    @LOGGER.catch
    def mobile_transformations(self, folder) -> List[Optional[str]]:
        """Generate mobile responsive images."""
        images_transformed = []
        LOGGER.info('Generating mobile images...')
        for image_blob in self.fetch_blobs(folder, image_type='retina'):
            new_image_name = image_blob.name.replace("@2x", "_mobile@2x")
            mobile_blob = self.bucket.blob(new_image_name)
            mobile_image = self._create_mobile_image(image_blob)
            mobile_blob.upload_from_string(mobile_image, content_type='image/jpeg')
            images_transformed.append(new_image_name)
        return images_transformed

    @LOGGER.catch
    def create_single_retina_image(self, image_url):
        """Create retina version of single image."""
        image_path = image_url.replace(self.bucket_url, '')
        image_blob = storage.Blob(image_path, self.bucket)
        new_image_name = image_blob.name.replace('.jpg', '@2x.jpg')
        existing_image_file = self._fetch_image_via_http(new_image_name)
        if existing_image_file is None:
            LOGGER.info(f'Creating retina image {new_image_name}')
            self._create_retina_image(image_blob, new_image_name)
        return f'{self.bucket_http_url}{new_image_name}'

    def fetch_random_lynx_image(self):
        """Fetch random Lynx image from GCS bucket."""
        lynx_images = self.get(prefix='roundup')
        images = [f"{self.bucket_http_url}{image.name}" for image in lynx_images if '@2x.jpg' in image.name]
        rand = randint(0, len(images) - 1)
        image = images[rand]
        LOGGER.info(f'Selected random Lynx image {image}')
        return image

    def _create_mobile_image(self, image_blob):
        """Create mobile responsive version of a given image."""
        image_file = self._fetch_image_via_http(image_blob)
        img_bytes = io.BytesIO()
        im = Image.open(BytesIO(image_file))
        im = im.resize((floor(im.width / 2), floor(im.height / 2)))
        im.save(img_bytes, format='JPEG')
        return img_bytes.getvalue()

    @LOGGER.catch
    def _create_retina_image(self, image_blob, new_image_name):
        """Create retina versions of standard-res images."""
        original_image = self._fetch_image_via_http(new_image_name)
        if original_image:
            img = Image.open(BytesIO(original_image))
            img.save()
            width, height = img.size
            if width > 1000:
                self.bucket.copy_blob(image_blob, self.bucket, new_image_name)

    @LOGGER.catch
    def _fetch_image_via_http(self, image_name):
        """Fetch raw image data via HTTP request."""
        url = f'{self.bucket_http_url}{image_name}'
        LOGGER.info(f'Checking {url}')
        image_request = requests.get(url)
        if image_request.headers['Content-Type'] in ('application/octet-stream', 'image/jpeg'):
            return image_request.content
        return None
