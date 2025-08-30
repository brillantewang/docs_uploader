import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Google Cloud Configuration
    DOCS_UPLOADER_PROJECT_ID = os.getenv('DOCS_UPLOADER_PROJECT_ID')
    print(os.getenv('DOCS_UPLOADER_PROJECT_ID'), 'DOCS_UPLOADER_PROJECT_ID')
    LOCATION = os.getenv('LOCATION', 'us')

    # Document AI Processor IDs
    MA_DOCS_CLASSIFIER_PROCESSOR_ID = os.getenv('MA_DOCS_CLASSIFIER_PROCESSOR_ID')
    MA_SALARY_TRANSACTION_EXTRACTOR_PROCESSOR_ID = os.getenv('MA_SALARY_TRANSACTION_EXTRACTOR_PROCESSOR_ID')

    # Google Drive Folder IDs
    MA_SALARY_TRANSACTION_G_DRIVE_FOLDER_ID = os.getenv('MA_SALARY_TRANSACTION_G_DRIVE_FOLDER_ID')

    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')

    # Application Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 8000))

config = Config()
