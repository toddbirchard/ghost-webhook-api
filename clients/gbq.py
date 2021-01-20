"""Bigquery client."""
from google.cloud import bigquery as google_bigquery


def bigquery(gcp_project: str, gcp_creds: str):
    """Instantiate Google BigQuery client."""
    return google_bigquery.Client(project=gcp_project, credentials=gcp_creds)
