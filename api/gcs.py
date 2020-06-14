"""Remote Google Cloud Storage client."""
from google.cloud import storage


class GCS:
    """Google Cloud Storage client."""

    def __init__(self, bucket_name, bucket_url, bucket_lynx):
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

    def get(self, prefix):
        """
        Retrieve all blobs in a bucket containing a prefix.
        :param prefix: Substring to match against filenames.
        :type prefix: str
        """
        return self.bucket.list_blobs(prefix=prefix)
