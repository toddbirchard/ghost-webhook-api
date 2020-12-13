from google.cloud import bigquery as google_bigquery


def bigquery(gcp_project, gcp_creds):
    return google_bigquery.Client(project=gcp_project, credentials=gcp_creds)
