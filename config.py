import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Google Cloud Configuration
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    PROJECT_ID = os.getenv('PROJECT_ID')
    LOCATION = os.getenv('LOCATION', 'us')
    PROCESSOR_ID = os.getenv('PROCESSOR_ID')
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')

    # Application Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 8000))

config = Config()
