"""Bigquery client."""
from google.cloud import bigquery as google_bigquery


class BigQuery:
    """Google BigQuery data warehouse client."""

    def __init__(self, basedir: str):
        self.basedir = basedir

    def create_client(self):
        """Instantiate Google BigQuery client."""
        return google_bigquery.Client.from_service_account_json(
            f"{self.basedir}/gcloud.json"
        )
