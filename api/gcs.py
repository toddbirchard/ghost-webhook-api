"""Connect to remote Google Cloud Storage client."""
from google.cloud import storage


class GCS:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    @property
    def client(self):
        return storage.Client()

    @property
    def bucket(self):
        return self.client.get_bucket(self.bucket_name)

    def get(self, prefix):
        """
        Retrieve all blobs in a bucket containing a prefix.

        :param prefix: Substring to match against filenames.
        :type prefix: str
        """
        return self.bucket.list_blobs(prefix=prefix)

    def purge_images(self, substrings, image_blobs):
        """Remove unused images."""
        for image_blob in image_blobs:
            if any(substr in image_blob.name for substr in substrings):
                self.bucket.delete_blob(image_blob.name)
                print(f'deleted {image_blob.name}')
