"""Connect to remote Google Cloud Storage bucket."""
from google.cloud import storage


def GCS(bucket_name):
    """Return a GCP bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    return bucket
