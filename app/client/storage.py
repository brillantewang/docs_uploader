from fastapi import File
from google.cloud import storage
from google.cloud.storage import fileio
from app.config import config

class Storage:
    def __init__(self):
        self.client = storage.Client(project=config.DOCS_UPLOADER_PROJECT_ID)
        self.bucket = self.client.bucket(config.GCS_BUCKET_NAME)

    def upload(self, file_name: str, file: File, content_type: str):
        try:
            blob = self.bucket.blob(blob_name=file_name)
            blob.upload_from_file(file_obj=file, content_type=content_type)
            print(f'Successfully uploaded to gs://{config.GCS_BUCKET_NAME}/{file_name}')
        except Exception as upload_error:
            print(f'Error uploading to gs://{config.GCS_BUCKET_NAME}/{file_name}: {upload_error}')

    def open(self, file_name: str) -> fileio.BlobReader:
        blob = self.bucket.blob(blob_name=file_name)
        return blob.open(mode='rb')
