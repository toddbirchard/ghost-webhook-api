from clients.database import Database
from clients.gcs import GCS
from clients.ghost import Ghost
from clients.sms import Twilio
from config import Config
from google.cloud import bigquery as bigquery_client


# Initialize clients
db = Database(
    uri=Config.SQLALCHEMY_DATABASE_URI,
    args=Config.SQLALCHEMY_ENGINE_OPTIONS
)
gcs = GCS(
    bucket_name=Config.GCP_BUCKET_NAME,
    bucket_url=Config.GCP_BUCKET_URL,
    bucket_lynx=Config.GCP_LYNX_DIRECTORY
)
# gbq = BigQuery(Config.GCP_BIGQUERY_URI)
ghost = Ghost(
    base_url=Config.GHOST_API_BASE_URL,
    version=3,
    client_id=Config.GHOST_CLIENT_ID,
    client_secret=Config.GHOST_ADMIN_API_KEY,
 )
sms = Twilio(Config)
bigquery = bigquery_client.Client()
