"""Remote Google Cloud Storage client."""
from math import floor
from google.cloud import storage
from random import randint
from io import BytesIO
import requests
from PIL import Image
from clients.log import LOGGER


class GCS:
    """Google Cloud Storage client."""

    def __init__(
            self,
            bucket_name: str,
            bucket_url: str,
            bucket_lynx: str
    ):
        self.bucket_name = bucket_name
        self.bucket_url = bucket_url
        self.bucket_lynx = bucket_lynx
        self.num_images_checked = 0
        self.images_total = 0

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

    def fetch_image_blobs(self, folder, image_type=None):
        """Retrieve images from GCS bucket matching directory & filter conditions."""
        files = self.get(prefix=folder)
        if image_type == 'retina':
            return [file for file in files if '@2x.jpg' in file.name]
        return [file for file in files if '@2x' not in file.name]

    def bulk_transform_images(self, folder, standard_images, retina_images):
        """Image transformation jobs."""
        self.num_images_checked = 0
        self.images_total = len(standard_images) + len(retina_images)
        self._purge_unwanted_images(folder)
        retina_transformed = self.retina_transformations(standard_images)
        mobile_transformed = self.mobile_transformations(retina_images)
        return retina_transformed, mobile_transformed

    @LOGGER.catch
    def _purge_unwanted_images(self, folder):
        """Delete images which have been compressed or generated multiple times."""
        LOGGER.info('Step 1: Purging unwanted images...')
        substrings = ['@2x@2x', '_o', 'psd', '?', '_mobile_mobile']
        image_blobs = self.get(folder)
        for image_blob in image_blobs:
            if any(substr in image_blob.name for substr in substrings):
                self.bucket.delete_blob(image_blob.name)
                LOGGER.info(f'Deleted {image_blob.name}.')
        return self.get(folder)

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
                    self.bucket.copy_blob(image_blob, self.bucket, standard_image_name)
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
                self.bucket.copy_blob(image_blob, self.bucket, new_image_name)
                images_transformed += 1
        return images_transformed

    @LOGGER.catch
    def create_single_retina_image(self, image_url):
        """Create retina version of single image."""
        image_path = image_url.replace(self.bucket_url, '')
        image_blob = storage.Blob(image_path, self.bucket)
        dot_position = image_blob.name.rfind('.')
        new_image_name = image_blob.name[:dot_position] + '@2x' + image_blob.name[dot_position:]
        existing_image_file = self._fetch_image_via_http(new_image_name)
        if existing_image_file is None:
            LOGGER.info(f'Creating retina image {new_image_name}')
            self._create_retina_image(image_blob, new_image_name)
        return f'{self.bucket_http_url}{new_image_name}'

    @LOGGER.catch
    def mobile_transformations(self, retina_images):
        images_transformed = 0
        for image_blob in retina_images:
            LOGGER.info(f'Making mobile version of {image_blob.name}')
            new_image_name = image_blob.name.replace("@2x", "_mobile@2x")
            blob = self.bucket.blob(new_image_name)
            original_image = self._fetch_image_via_http(image_blob.name)
            if original_image:
                im = Image.open(BytesIO(original_image))
                width, height = im.size
                if width > 1000:
                    im_resized = im.resize((floor(im.width/2), floor(im.height/2)))
                    local_file = f'api/images/tmp/{new_image_name.split("/")[-1]}'
                    im_resized.save(local_file, format='JPEG2000')
                    blob.upload_from_filename(local_file)
                    LOGGER.info(f'Created mobile version of {image_blob.name}.')
                    images_transformed += 1
        return images_transformed

    def fetch_random_lynx_image(self):
        """Fetch random Lynx image from GCS bucket."""
        lynx_images = self.get(prefix='roundup')
        images = [f"{self.bucket_http_url}{image.name}" for image in lynx_images if '@2x.jpg' in image.name]
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
            img.save()
            width, height = img.size
            if width > 1000:
                self.bucket.copy_blob(image_blob, self.bucket, new_image_name)

    @LOGGER.catch
    def _fetch_image_via_http(self, new_image_name):
        """Determine if image exists via HTTP request."""
        LOGGER.info(f'Checking {self.bucket_http_url}{new_image_name}')
        image_request = requests.get(self.bucket_http_url, new_image_name)
        if image_request.headers['Content-Type'] in ('application/octet-stream', 'image/jpeg'):
            return image_request.content
        return None
