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
