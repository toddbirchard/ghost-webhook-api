"""Connect to remote GCP bucket containing images."""
from google.cloud import storage


def GCS(bucket_name):
    """Return a GCP bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    return bucket
