"""Connect to remote Google Cloud Storage client."""
from google.cloud import storage


class GCS:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    @property
    def client(self):
        """Google Cloud Storage client."""
        return storage.Client()

    @property
    def bucket(self):
        """Google Cloud Storage bucket where memes are stored."""
        return self.client.get_bucket(self.bucket_name)

    def get(self, prefix):
        """
        Retrieve all blobs in a bucket containing a prefix.

        :param prefix: Substring to match against filenames.
        :type prefix: str
        """
        return self.bucket.list_blobs(prefix=prefix)

