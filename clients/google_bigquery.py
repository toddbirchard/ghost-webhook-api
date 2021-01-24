"""Bigquery client."""
from google.cloud import bigquery as google_bigquery


class BigQuery:
    """Google BigQuery data warehouse client."""

    def __init__(self, gcp_project: str, gcp_creds: str):
        self.gcp_project = gcp_project
        self.gcp_creds = gcp_creds

    def create_client(self):
        """Instantiate Google BigQuery client."""
        return google_bigquery.Client(
            project=self.gcp_project, credentials=self.gcp_creds
        )
