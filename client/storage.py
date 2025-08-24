from fastapi import File
from google.cloud import storage
from config import config

class Storage:
    def __init__(self):
        self.client = storage.Client(project=config.PROJECT_ID)
        self.bucket = self.client.bucket(config.GCS_BUCKET_NAME)

    def upload(self, file_name: str, file: File):
        try:
            blob = self.bucket.blob(blob_name=file_name)
            blob.upload_from_file(file_obj=file)
            print(f'Successfully uploaded to gs://{config.GCS_BUCKET_NAME}/{file_name}')
        except Exception as upload_error:
            print(f'Error uploading to gs://{config.GCS_BUCKET_NAME}/{file_name}: {upload_error}')
