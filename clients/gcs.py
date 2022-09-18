"""Google Cloud Storage client and image transformer."""
import re
from typing import Iterator, Tuple

from google.cloud import storage
from google.cloud.storage.blob import Blob
from google.cloud.storage.client import Bucket, Client

from log import LOGGER


class GCS:
    """Google Cloud Storage image CDN."""

    def __init__(
        self,
        gcp_project_name: str,
        gcp_api_credentials: str,
        bucket_name: str,
        bucket_url: str,
    ):
        self.gcp_project_name = gcp_project_name
        self.gcp_api_credentials = gcp_api_credentials
        self.bucket_name = bucket_name
        self.bucket_url = bucket_url

    @property
    def client(self) -> Client:
        """
        Google Cloud Storage client.

        :returns: Client
        """
        return storage.Client(
            project=self.gcp_project_name,
            credentials=self.gcp_api_credentials,
        )

    @property
    def bucket(self) -> Bucket:
        """
        Google Cloud Storage bucket where images are stored.

        :returns: Bucket
        """
        return self.client.get_bucket(self.bucket_name)

    @property
    def bucket_http_url(self) -> str:
        """
        Publicly accessible HTTP URL for images.

        :returns: str
        """
        return self.bucket_url

    def get(self, prefix: str) -> Iterator:
        """
        Retrieve all blobs in a bucket containing a prefix.

        :param str prefix: Substring to match against filenames.

        :returns: Iterator
        """
        return self.client.list_blobs(self.bucket, prefix=prefix)

    def _remove_repeat_blobs(self, image_blobs):
        images_purged = []
        r = re.compile("-[0-9]-[0-9]@2x.jpg")
        repeat_blobs = list(filter(r.match, image_blobs))
        for repeat_blob in repeat_blobs:
            self.bucket.delete_blob(repeat_blob)
            images_purged.append(repeat_blob)
            LOGGER.info(f"Deleted {repeat_blob}")

    @staticmethod
    def _get_folder_and_filename(image_blob: Blob) -> Tuple[str, str]:
        """
        Get relative file path & filename from a given blob.

        :param Blob image_blob: Blob representing an image file stored on GCS.

        :returns: Tuple[str, str]
        """
        image_folder = image_blob.name.rsplit("/", 1)[0]
        image_name = image_blob.name.rsplit("/", 1)[1]
        return image_folder, image_name

    """def image_headers(self, folder: str) -> List:
        header_blobs = []
        image_blobs = [blob for blob in self.selects(folder)]
        for image_blob in image_blobs:
            if ".jpg" in image_blob.name and "octet-stream" in image_blob.content_type:
                image_blob.content_type = "image/jpg"
                self.bucket.copy_blob(image_blob, self.bucket, )
                header_blobs.append(image_blob.name)
                self.bucket.blob(image_blob.name).update({"Content-Type": "image/jpg"})
                # .delete(image_blob)
                LOGGER.info(f"Applied content-type `image/jpg` to {image_blob.name}")
            elif (
                ".png" in image_blob.name and "octet-stream" in image_blob.content_type
            ):
                image_blob.content_type = "image/png"
                self.bucket.copy_blob(image_blob, self.bucket)
                header_blobs.append(image_blob.name)
                LOGGER.info(f"Applied content-type `image/png` to {image_blob.name}")
        return header_blobs"""
