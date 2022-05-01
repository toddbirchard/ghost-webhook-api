"""Image transformer for remote images on GCS."""
from io import BytesIO
from random import randint
from typing import List, Optional

from google.cloud.exceptions import GoogleCloudError
from google.cloud.storage.blob import Blob
from PIL import Image

from clients.gcs import GCS
from log import LOGGER


class ImageTransformer(GCS):
    """Image generator for images stored on GCS."""

    def __init__(
        self,
        gcp_project_name: str,
        gcp_api_credentials: str,
        bucket_name: str,
        bucket_url: str,
    ):
        super().__init__(gcp_project_name, gcp_api_credentials, bucket_name, bucket_url)

    def get_standard_blobs(self, folder: str) -> List[Optional[Blob]]:
        """
        Fetch all standard-res image blobs within a given directory.

        :param str folder: GCS filepath from which to scan for images.

        :returns: List[Optional[Blob]]
        """
        files = self.get(prefix=folder)
        files = list(files)
        return [
            file
            for file in files
            if "@2x" not in file.name
            and "/_retina" not in file.name
            and "/_mobile" not in file.name
            and "/authors" not in file.name
            and "/assets" not in file.name
        ]

    def _get_retina_blobs(self, directory: str) -> List[Blob]:
        """
        Retrieve retina image blobs from directory in GCS bucket.

        :param str directory: Directory from which to fetch blobs.

        :returns: List[Blob]
        """
        files = self.get(prefix=directory)
        return [
            file for file in files if "@2x" in file.name and "/_retina" in file.name
        ]

    @LOGGER.catch
    def organize_retina_images(self, folder: str) -> List:
        """
        Move images into their respective folders.

        :param str folder: Directory to recursively apply image transformations.

        :returns: List
        """
        moved_blobs = []
        image_blobs = self._get_retina_blobs(folder)
        for image_blob in image_blobs:
            image_folder, image_name = self._get_folder_and_filename(image_blob)
            if "/_retina/" in image_name:
                pass
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

    @LOGGER.catch
    def purge_unwanted_images(self, folder: str) -> List[str]:
        """
        Delete images which have been compressed or generated multiple times.

        :param str folder: Directory to recursively apply image transformations.

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
            "_retina/_mobile/",
        ]
        blobs = self.get(
            folder,
        )
        image_blob_names = [blob.name for blob in blobs]
        for image_blob_name in image_blob_names:
            if any(substr in image_blob_name for substr in substrings):
                self.bucket.delete_blob(image_blob_name)
                images_purged.append(image_blob_name)
                LOGGER.info(f"Deleted {image_blob_name}.")
        return images_purged

    @LOGGER.catch
    def retina_transformations(self, folder: str) -> List[Optional[str]]:
        """
        Create retina image variants of standard-res images.

        :param str folder: Directory to recursively apply image transformations.

        :returns: List[Optional[str]]
        """
        images_transformed = []
        image_blobs = self.get_standard_blobs(folder)
        LOGGER.info(f"Creating retina variants for {len(image_blobs)} images...")
        for image_blob in image_blobs:
            retina_image_blob = self.create_retina_image(image_blob)
            if retina_image_blob is not None:
                images_transformed.append(retina_image_blob.name)
        return images_transformed

    def create_retina_image(self, image_blob: Blob) -> Optional[Blob]:
        """
        Create a single retina image variant of a standard-res image.

        :param Blob image_blob: Image blob object.

        :returns: Optional[Blob]
        """
        image_folder, image_name = self._get_folder_and_filename(image_blob)
        retina_blob_filepath = f"{image_folder}/_retina/{image_name.replace('.jpg', '@2x.jpg').replace('.png', '@2x.png')}"
        retina_image_blob = self.bucket.blob(retina_blob_filepath)
        if retina_image_blob.exists() is False:
            self.bucket.copy_blob(
                image_blob, self.bucket, new_name=retina_blob_filepath
            )
            new_retina_image_blob = self.bucket.blob(retina_blob_filepath)
            LOGGER.success(f"Created retina image `{retina_blob_filepath}`")
            return new_retina_image_blob
        else:
            LOGGER.info(
                f"Skipping retina image `{retina_blob_filepath}`; already exists."
            )
        return None

    @LOGGER.catch
    def mobile_transformations(self, folder: str) -> List[Optional[str]]:
        """
        Create mobile image variants of standard-res images.

        :param str folder: Directory to recursively apply image transformations.

        :returns: List[Optional[str]]
        """
        images_transformed = []
        image_blobs = self.get_standard_blobs(folder)
        LOGGER.info(f"Creating mobile variants for {len(image_blobs)} images...")
        for image_blob in image_blobs:
            mobile_image_blob = self.create_mobile_image(image_blob)
            if mobile_image_blob is not None:
                images_transformed.append(mobile_image_blob.name)
        return images_transformed

    def create_mobile_image(self, image_blob: Blob) -> Optional[Blob]:
        """
        Create single mobile image variant for a given image blob.

        :param Blob image_blob: Standard resolution image blob from which to create retina image.

        :returns: Optional[Blob]
        """
        image_folder, image_name = self._get_folder_and_filename(image_blob)
        mobile_blob_filepath = f"{image_folder}/_mobile/{image_name.replace('.jpg', '@2x.jpg').replace('.png', '@2x.png')}"
        mobile_image_blob = self.bucket.blob(mobile_blob_filepath)
        if mobile_image_blob.exists() is False:
            new_mobile_image_blob = self._transform_mobile_image(
                image_blob, mobile_image_blob
            )
            return new_mobile_image_blob
        else:
            LOGGER.info(
                f"Skipping mobile image `{mobile_blob_filepath}`; already exists."
            )
        return None

    @staticmethod
    def _get_image_meta(blob: Blob) -> Optional[dict]:
        """
        Generate metadata for a given image Blob.

        :param Blob blob: Image blob being transformed.

        :returns: Optional[dict]
        """
        if ".jpg" in blob.name:
            return {"format": "JPEG", "content-type": "image/jpg"}
        elif ".png" in blob.name:
            return {"format": "PNG", "content-type": "image/png"}
        return None

    def _transform_mobile_image(
        self, original_image_blob: Blob, new_image_blob: Blob
    ) -> Optional[Blob]:
        """
        Create smaller image size to be served on mobile devices.

        :param Blob original_image_blob: Original image blob.
        :param Blob new_image_blob: New newly created Blob for mobile image.

        :returns: Optional[Blob]
        """
        img_meta = self._get_image_meta(original_image_blob)
        img_bytes = original_image_blob.download_as_bytes()
        if img_bytes:
            stream = BytesIO(img_bytes)
            im = Image.open(stream)
            try:
                with BytesIO() as output:
                    new_image = im.reduce(2)
                    new_image.save(output, format=img_meta["format"])
                    new_image_blob.upload_from_string(
                        output.getvalue(), content_type=img_meta["content-type"]
                    )
                    LOGGER.success(f"Created mobile image `{new_image_blob.name}`")
                    return new_image_blob
            except GoogleCloudError as e:
                LOGGER.error(
                    f"GoogleCloudError while saving mobile image `{new_image_blob.name}`: {e}"
                )
            except Exception as e:
                LOGGER.error(
                    f"Unexpected exception while saving mobile image `{new_image_blob.name}`: {e}"
                )

    @staticmethod
    def _add_image_headers(image_blob: Blob):
        if ".jpg" in image_blob.name and "octet-stream" in image_blob.content_type:
            image_blob.content_type = "image/jpg"
        elif ".png" in image_blob.name and "octet-stream" in image_blob.content_type:
            image_blob.content_type = "image/png"
        return image_blob
