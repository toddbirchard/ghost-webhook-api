"""Creates missing image formats in a Google Cloud CDN."""
import requests
from io import BytesIO
from PIL import Image
from flask import current_app as api
from api import gcs


class ImageTransformer:

    def __init__(self, bucket_name, bucket_url, retina_images, standard_images):
        self.bucket_name = bucket_name
        self.bucket_url = bucket_url
        self.retina_images = retina_images
        self.standard_images = standard_images
        self.num_images_checked = 0
        self.images_total = len(self.retina_images) + len(self.standard_images)
        self.retina_images_transformed = []
        self.standard_images_transformed = []
        self.webp_images_transformed = []

    def retina_transform(self):
        """Find images missing a retina-quality counterpart."""
        for image_blob in self.standard_images:
            self.num_images_checked += 1
            api.logger.info(f'{self.num_images_checked} of {self.images_total} ({image_blob.name})')
            dot_position = image_blob.name.rfind('.')
            new_image_name = image_blob.name[:dot_position] + '@2x' + image_blob.name[dot_position:]
            existing_image_file = self.__fetch_image_via_http(new_image_name)
            if existing_image_file is None:
                self.__create_retina_image(image_blob, new_image_name)
        return self.retina_images_transformed

    def standard_transform(self):
        """Find images missing a standard-res counterpart."""
        for image_blob in self.retina_images:
            self.num_images_checked += 1
            api.logger.info(f'{self.num_images_checked} of {self.images_total} ({image_blob.name})')
            if '@2x' in image_blob.name:
                standard_image_name = image_blob.name.replace('@2x', '')
                standard_image = self.__fetch_image_via_http(standard_image_name)
                if standard_image is not None:
                    new_blob = gcs.copy_blob(image_blob, gcs, standard_image_name)
                    self.standard_images_transformed.append(new_blob.name)
        return self.standard_images_transformed

    def webp_transform(self):
        """Find images missing a webp counterpart."""
        for image_blob in self.retina_images:
            self.num_images_checked += 1
            api.logger.info(f'{self.num_images_checked} of {self.images_total} ({image_blob.name})')
            new_image_name = image_blob.name.split('.')[0] + '.webp'
            image_file = self.__fetch_image_via_http(new_image_name)
            if image_file is not None:
                new_blob = gcs.copy_blob(image_blob, gcs, new_image_name)
                self.webp_images_transformed.append(new_blob.name)
        return self.webp_images_transformed

    def __create_retina_image(self, image_blob, new_image_name):
        """Create retina versions of standard-res images."""
        original_image = self.__fetch_image_via_http(image_blob.name)
        im = Image.open(BytesIO(original_image))
        width, height = im.size
        if width > 1000:
            new_blob = gcs.copy_blob(image_blob, gcs, new_image_name)
            self.retina_images_transformed.append(new_blob.name)

    def __fetch_image_via_http(self, url):
        """Determine if image exists via HTTP request."""
        image_request = requests.get(self.bucket_url + url)
        if image_request.headers['Content-Type'] in ('application/octet-stream', 'image/jpeg'):
            return image_request.content
        return None
