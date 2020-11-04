"""Google Cloud Storage client and image transformer."""
import io
import re
from io import BytesIO
from random import randint
from typing import List, Optional

import requests
from google.cloud import storage
from google.cloud.storage.blob import Blob
from PIL import Image

from clients.log import LOGGER


class GCS:
    """Google Cloud Storage image CDN."""

    def __init__(self, bucket_name: str, bucket_url: str, bucket_lynx: str):
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
    def bucket_http_url(self) -> str:
        """Publicly accessible URL for images.."""
        return self.bucket_url

    def get(self, prefix: str) -> List[Blob]:
        """
        Retrieve all blobs in a bucket containing a prefix.

        :param prefix: Substring to match against filenames.
        :type prefix: str

        :returns: List[Blob]
        """
        return self.bucket.list_blobs(prefix=prefix)

    def fetch_blobs(
        self, folder: str, image_type: Optional[str] = None
    ) -> List[Optional[Blob]]:
        """
        Retrieve images from GCS bucket matching directory & filter conditions.

        :param folder: Remote directory to recursively apply image transformations,=.
        :type folder: str
        :param image_type: Type of image transformation to apply.
        :type image_type: Optional[str]

        :returns: List[Blob]
        """
        files = self.get(prefix=folder)
        if image_type == "retina":
            return [
                file
                for file in files
                if "@2x.jpg" in file.name and "_mobile" not in file.name and '/retina' not in file.name
            ]
        return [
            file
            for file in files
            if "@2x" not in file.name and "_mobile" not in file.name
        ]

    @LOGGER.catch
    def purge_unwanted_images(self, folder: str) -> List[str]:
        """
        Delete images which have been compressed or generated multiple times.

        :param folder: Remote directory to recursively apply image transformations.
        :type folder: str

        :returns: List[str]
        """
        images_purged = []
        LOGGER.info("Purging unwanted images...")
        substrings = ["@2x@2x", "_o", "psd", "?", "_mobile", "@2x-", "-1-1", "-1-2"]
        blobs = self.get(folder)
        image_blobs = [blob.name for blob in blobs]
        for image_blob in image_blobs:
            if any(substr in image_blob for substr in substrings):
                self.bucket.delete_blob(image_blob)
                images_purged.append(image_blob)
                LOGGER.info(f"Deleted {image_blob}")
            r = re.compile("-[0-9]-[0-9]@2x.jpg")
            repeat_blobs = list(filter(r.match, image_blobs))
            for repeat_blob in repeat_blobs:
                self.bucket.delete_blob(repeat_blob)
                images_purged.append(repeat_blob)
                LOGGER.info(f"Deleted {repeat_blob}")
        return images_purged

    def organize_retina_images(self, folder: str) -> List:
        """Move retina images into retina folder."""
        moved_blobs = []
        image_blobs = [blob for blob in self.get(folder) if '@2x' in blob.name and '/mobile' not in blob.name]
        for image_blob in image_blobs:
            if '/retina' not in image_blob.name:
                image_folder = image_blob.name.rsplit('/', 1)[0]
                image_name = image_blob.name.rsplit('/', 1)[1]
                moved_blob = self.bucket.blob(f'{image_folder}/retina/{image_name}')
                if moved_blob.exists() is not None:
                    moved_blob = self.bucket.copy_blob(image_blob, self.bucket, new_name=moved_blob.name)
                    image_blob.delete()
                    moved_blobs.append(moved_blob.name)
                    LOGGER.info(f"Moved image `{moved_blob.name}`")
        return moved_blobs

    def organize_mobile_images(self, folder: str) -> List:
        """Move retina images into retina folder."""
        moved_blobs = []
        image_blobs = [blob for blob in self.get(folder) if '_mobile' in blob.name and '/retina' not in blob.name]
        for image_blob in image_blobs:
            if '/mobile' not in image_blob.name:
                image_folder = image_blob.name.rsplit('/', 1)[0]
                image_name = image_blob.name.rsplit('/', 1)[1]
                moved_blob = self.bucket.blob(f'{image_folder}/mobile/{image_name}')
                if moved_blob.exists() is not None:
                    moved_blob = self.bucket.copy_blob(image_blob, self.bucket, new_name=moved_blob.name)
                    image_blob.delete()
                    moved_blobs.append(moved_blob.name)
                    LOGGER.info(f"Moved image `{moved_blob.name}`")
        return moved_blobs

    def image_headers(self, folder: str) -> List:
        header_blobs = []
        image_blobs = [blob for blob in self.get(folder)]
        for image_blob in image_blobs:
            if '.jpg' in image_blob.name and 'octet-stream' in image_blob.content_type:
                image_blob.content_type = 'image/jpg'
                self.bucket.copy_blob(image_blob, self.bucket)
                header_blobs.append(image_blob.name)
            elif '.png' in image_blob.name and 'octet-stream' in image_blob.content_type:
                image_blob.content_type = 'image/png'
                self.bucket.copy_blob(image_blob, self.bucket)
                header_blobs.append(image_blob.name)
        return header_blobs

    def retina_transformations(self, folder: str) -> List[Optional[str]]:
        """Find images missing a retina-quality counterpart."""
        images_transformed = []
        LOGGER.info("Generating retina images...")
        for image_blob in self.fetch_blobs(folder):
            new_image_name = image_blob.name.replace(".jpg", "@2x.jpg")
            mobile_blob = self.bucket.blob(new_image_name)
            if mobile_blob.exists() is False:
                self._new_image_blob(image_blob, image_type='retina')
                images_transformed.append(mobile_blob.name)
        return images_transformed

    @LOGGER.catch
    def mobile_transformations(self, folder: str) -> List[Optional[str]]:
        """
        Generate mobile responsive images.

        :param folder: Remote directory to recursively apply image transformations,=.
        :type folder: str

        :returns: List[str]
        """
        images_transformed = []
        LOGGER.info("Generating mobile images...")
        for image_blob in self.fetch_blobs(folder, image_type="retina"):
            mobile_blob = self._new_image_blob(image_blob, image_type='mobile')
            if mobile_blob.exists() is False:
                mobile_blob_bytes = self._create_mobile_image(image_blob)
                mobile_blob.upload_from_string(mobile_blob_bytes, content_type="image/jpeg")
                images_transformed.append(mobile_blob.name)
        return images_transformed

    @LOGGER.catch
    def create_single_retina_image(self, image_url: str) -> str:
        """
        Create retina version of single image.

        :param image_url: Generate single retina image from remote image URL.
        :type image_url: str

        :returns: str
        """
        relative_image_path = image_url.replace(self.bucket_url, "")
        original_image_blob = storage.Blob(relative_image_path, self.bucket)
        retina_blob = self._new_image_blob(original_image_blob, image_type='retina')
        self._create_retina_image(original_image_blob, retina_blob)
        return f"{self.bucket_http_url}{retina_blob.name}"

    def _new_image_blob(self, image_blob: Blob, image_type=None) -> Optional[Blob]:
        """
        :param image_blob: Google storage blob representing an image.
        :type image_blob: Blob

        :returns: Blob
        """
        image_folder = image_blob.name.rsplit('/', 1)[0]
        image_name = image_blob.name.rsplit('/', 1)[1]
        if image_type == 'mobile':
            mobile_blob = self.bucket.blob(f'{image_folder}/{image_type}/{image_name}')
            if mobile_blob.exists() is False:
                return mobile_blob
        elif image_blob.exists() is False and image_type == 'retina':
            image_name = image_name.replace(".jpg", "@2x.jpg")
            image_blob = self.bucket.blob(f'{image_folder}/{image_type}/{image_name}')
            self.bucket.copy_blob(image_blob, self.bucket, image_blob)
            LOGGER.info(f"Created retina image `{image_blob.name}`")
            return image_blob
        elif image_blob.exists() is True and image_type is not None:
            LOGGER.info(f"{image_blob.name} already exists.")
        return None

    def fetch_random_lynx_image(self) -> str:
        """Fetch random Lynx image from GCS bucket."""
        lynx_images = self.get(prefix="roundup")
        images = [
            f"{self.bucket_http_url}{image.name}"
            for image in lynx_images
            if "@2x.jpg" in image.name
            and '_mobile' not in image.name
        ]
        rand = randint(0, len(images) - 1)
        image = images[rand]
        LOGGER.info(f"Selected random Lynx image: `{image}`")
        return image

    def _create_mobile_image(self, image_blob: Blob) -> Optional[bytes]:
        """
        Create smaller image size to be served on mobile devices.

        :param image_blob: Original image blob.
        :type image_blob: Blob

        :returns: Optional[bytes]
        """
        img_bytes = self._fetch_image_via_http(image_blob.name)
        if img_bytes:
            stream = BytesIO(img_bytes)
            im = Image.open(stream)
            width, height = im.size
            if width > 1000:
                im_resized = im.resize((600, 346))
                new_image_bytes = io.BytesIO()
                im_resized.save(new_image_bytes, "JPEG", quality=90, optimize=True)
                return new_image_bytes.getvalue()
        return None

    @LOGGER.catch
    def _create_retina_image(self, original_blob: Blob, retina_blob: Blob) -> Optional[str]:
        """
        Create retina versions of standard-res images.

        :param original_blob: Original image blob.
        :type original_blob: Blob
        :param retina_blob: New blob target for image creation.
        :type retina_blob: Blob
        """
        original_image_file = self._fetch_image_via_http(original_blob.name)
        if original_image_file is not None:
            im = Image.open(BytesIO(original_image_file))
            width, height = im.size
            if width > 1000:
                return self.bucket.copy_blob(original_blob, self.bucket, retina_blob.name)
        return None

    @LOGGER.catch
    def _fetch_image_via_http(self, image_name: str) -> Optional[bytes]:
        """
        Fetch raw image data via HTTP request.

        :param image_name: Filepath of image to retrieve.
        :type image_name: str

        :returns: Optional[bytes]
        """
        url = f"{self.bucket_http_url}{image_name}"
        image_request = requests.get(url)
        if image_request.headers["Content-Type"] in (
            "application/octet-stream",
            "image/jpeg",
        ):
            return image_request.content
        return None
