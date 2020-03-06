"""App configuration."""
from os import environ
import datetime
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Set Flask configuration vars from .env file."""
    dt = datetime.datetime.today()

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_PEM = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_ENGINE_OPTIONS = {'ssl': {'ca': './creds/ca-certificate.crt'}}

    # Algolia API
    ALGOLIA_BASE_URL = environ.get('ALGOLIA_BASE_URL')
    ALGOLIA_APP_ID = environ.get('ALGOLIA_APP_ID')
    ALGOLIA_API_KEY = environ.get('ALGOLIA_API_KEY')

    # Google Cloud storage
    GCP_BUCKET_URL = environ.get('GCP_BUCKET_URL')
    GCP_BUCKET_NAME = environ.get('GCP_BUCKET_NAME')
    GOOGLE_APPLICATION_CREDENTIALS = './creds/gcloud.json'
    GCP_BUCKET_FOLDER = [f'{dt.year}/{dt.strftime("%m")}']

    # Ghost
    GHOST_API_BASE_URL = environ.get('GHOST_API_BASE_URL')
    GHOST_API_USERNAME = environ.get('GHOST_API_USERNAME')
    GHOST_API_PASSWORD = environ.get('GHOST_API_PASSWORD')
    GHOST_API_KEY = environ.get('GHOST_API_KEY')
    GHOST_API_EXPORT_URL = f'{GHOST_API_BASE_URL}/admin/db/'
