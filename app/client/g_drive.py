from google.cloud.storage import fileio
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from constants import DOCUMENT_TYPE_TO_G_DRIVE_FOLDER
from global_types import DocumentType
from typing import TypedDict

SCOPES = ['https://www.googleapis.com/auth/drive']

class UploadFileResponse(TypedDict):
    id: str

class GoogleDrive:
    def __init__(self):
        self.client = build('drive', 'v3')

    def upload_file(self, file: fileio.BlobReader, output_file_name: str, document_type: DocumentType) -> UploadFileResponse:
        file_metadata = {
            'name': output_file_name,
            'parents': [DOCUMENT_TYPE_TO_G_DRIVE_FOLDER[document_type]]
        }

        media_body = MediaIoBaseUpload(
            fd=file,
            mimetype=file._blob._get_content_type(content_type=None)
        )

        response = self.client.files().create(
            body=file_metadata,
            media_body=media_body
        ).execute()

        return { 'id': response['id'] }
