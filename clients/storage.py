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
                if "@2x.jpg" in file.name and "/_retina" in file.name
            ]
        return [
            file
            for file in files
            if "@2x" not in file.name and "/_mobile" not in file.name
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
        substrings = [
            "@2x@2x",
            "_o",
            "psd",
            "?",
            "@2x-",
            "-1-1",
            "-1-2",
            ".webp",
            "_retina/_retina",
        ]
        blobs = self.get(
            folder,
        )
        image_blobs = [blob for blob in blobs]
        for image_blob in image_blobs:
            if any(substr in image_blob.name for substr in substrings):
                self.bucket.delete_blob(image_blob)
                images_purged.append(image_blob.name)
                LOGGER.info(f"Deleted {image_blob.name}.")
            r = re.compile("-[0-9]-[0-9]@2x.jpg")
            repeat_blobs = list(filter(r.match, image_blobs))
            for repeat_blob in repeat_blobs:
                self.bucket.delete_blob(repeat_blob)
                images_purged.append(repeat_blob)
                LOGGER.info(f"Deleted {repeat_blob}")
        return images_purged

    def organize_retina_images(self, folder: str) -> List:
        """
        Move images into respective folder.

        :param folder: Remote directory to recursively apply image transformations.
        :type folder: str

        :returns: List
        """
        image_blobs = [
            blob
            for blob in self.get(folder)
            if "@2x" in blob.name and "/_retina" not in blob.name
        ]
        moved_blobs = []
        for image_blob in image_blobs:
            image_folder, image_name = self._get_folder_and_filename(image_blob)
            moved_blob = self.bucket.blob(f"{image_folder}/_retina/{image_name}")
            if moved_blob.exists() is False:
                moved_blob = self.bucket.copy_blob(
                    image_blob, self.bucket, new_name=moved_blob.name
                )
                image_blob.delete()
                moved_blobs.append(moved_blob.name)
                LOGGER.info(f"Moved `{image_blob.name}` -> `{moved_blob.name}`")
            LOGGER.info(f"Ignored moving `{moved_blob.name}`")
        return moved_blobs

    def image_headers(self, folder: str) -> List:
        header_blobs = []
        image_blobs = [blob for blob in self.get(folder)]
        for image_blob in image_blobs:
            if ".jpg" in image_blob.name and "octet-stream" in image_blob.content_type:
                image_blob.content_type = "image/jpg"
                self.bucket.copy_blob(image_blob, self.bucket)
                header_blobs.append(image_blob.name)
                LOGGER.info(f"Applied content-type `image/jpg` to {image_blob.name}")
            elif (
                ".png" in image_blob.name and "octet-stream" in image_blob.content_type
            ):
                image_blob.content_type = "image/png"
                self.bucket.copy_blob(image_blob, self.bucket)
                header_blobs.append(image_blob.name)
                LOGGER.info(f"Applied content-type `image/png` to {image_blob.name}")
        return header_blobs

    def retina_transformations(self, folder: str) -> List[Optional[str]]:
        """Find images missing a retina-quality counterpart."""
        images_transformed = []
        LOGGER.info("Generating retina images...")
        for image_blob in self.fetch_blobs(folder):
            new_image_name = image_blob.name.replace(".jpg", "@2x.jpg")
            mobile_blob = self.bucket.blob(new_image_name)
            if mobile_blob.exists() is False:
                self._new_image_blob(image_blob, "retina")
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
            mobile_blob = self._new_image_blob(image_blob, "mobile")
            images_transformed.append(mobile_blob)
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
        image_blob = storage.Blob(relative_image_path, self.bucket)
        retina_blob = self._new_image_blob(image_blob, "retina")
        return f"{self.bucket_http_url}{retina_blob}"

    def _new_image_blob(self, image_blob: Blob, image_type: str) -> Optional[str]:
        """
        :param image_blob: Google storage blob representing an image.
        :type image_blob: Blob
        :param image_type: Type of img transformation to apply.
        :type image_type: str

        :returns: Blob
        """
        image_folder, image_name = self._get_folder_and_filename(image_blob)
        if image_type == "retina":
            new_image_name = (
                f"{image_folder}/_{image_type}/{image_name.replace('.jpg', '@2x.jpg')}"
            )
            new_image_blob = self.bucket.blob(new_image_name)
            if new_image_blob.exists() is False:
                self.bucket.copy_blob(image_blob, self.bucket, new_image_name)
                LOGGER.info(f"Created retina image `{new_image_name}`")
                return new_image_name
        elif image_type == "mobile":
            new_image_name = (
                f"{image_folder.replace('/_retina', '/_mobile')}/{image_name}"
            )
            new_image_blob = self.bucket.blob(new_image_name)
            if new_image_blob.exists():
                self._create_mobile_image(image_blob, new_image_blob)
                LOGGER.info(f"Created mobile image `{new_image_name}`")
                return new_image_name
        return None

    def fetch_random_lynx_image(self) -> str:
        """Fetch random Lynx image from GCS bucket."""
        lynx_images = self.get(prefix="roundup")
        images = [
            f"{self.bucket_http_url}{image.name}"
            for image in lynx_images
            if "@2x.jpg" in image.name and "_mobile" not in image.name
        ]
        rand = randint(0, len(images) - 1)
        image = images[rand]
        LOGGER.info(f"Selected random Lynx image: `{image}`")
        return image

    def _create_mobile_image(
        self, original_image_blob: Blob, new_image_blob: Blob
    ) -> Optional[str]:
        """
        Create smaller image size to be served on mobile devices.

        :param original_image_blob: Original image blob.
        :type original_image_blob: Blob
        :param new_image_blob: New newly created Blob for mobile image.
        :type new_image_blob: Blob

        :returns: Optional[str]
        """
        img_bytes = self._fetch_image_via_http(original_image_blob.name)
        if img_bytes:
            stream = BytesIO(img_bytes)
            im = Image.open(stream)
            width, height = im.size
            if width > 1000:
                im_resized = im.resize((600, 346))
                new_image_bytes = io.BytesIO()
                im_resized.save(new_image_bytes, "JPEG", quality=90, optimize=True)
                content_type = original_image_blob.name.split(".", -1)[1]
                content_types = {
                    "jpg": "image/jpeg",
                    "png": "image/png",
                }
                new_image_blob.upload_from_string(
                    new_image_bytes.getvalue(), content_type=content_types[content_type]
                )
                return new_image_blob.name
        return None

    @staticmethod
    def _get_folder_and_filename(image_blob: Blob) -> (str, str):
        """
        Get relative file path & filename from a given blob.

        :param image_blob: Image stored on GCS
        :type image_blob: Blob

        :returns: (str, str)
        """
        image_folder = image_blob.name.rsplit("/", 1)[0]
        image_name = image_blob.name.rsplit("/", 1)[1]
        return image_folder, image_name

    @LOGGER.catch
    def _fetch_image_via_http(self, image_name: str) -> Optional[bytes]:
        """
        Fetch raw image data via HTTP request.

        :param image_name: Filepath of image to retrieve.
        :type image_name: str

        :returns: Optional[bytes]
        """
        url = f"{self.bucket_http_url}{image_name}"
        req = requests.get(url)
        if req.status_code == 200 and req.headers["Content-Type"] in (
            "application/octet-stream",
            "image/jpeg",
            "image/jpg",
            "image/png",
        ):
            return req.content
        return None
