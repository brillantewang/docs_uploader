from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

app = FastAPI()

class GDriveParts(BaseModel):
    document_type: str
    g_drive_file_name: str

@app.post('/documents/g_drive_parts')
async def create_g_drive_parts(document: UploadFile) -> GDriveParts:
    print(document.filename, 'filename')
    print(document.content_type, 'content type')
    # Hits classifier processor to get document type
    # Based on the document type
    # it sends that document to the corresponding extractor processor
    # It constructs the g_drive_file_name based on the extracted text
    # Returns the document_type and g_drive_file_name

    response = GDriveParts(document_type='dog', g_drive_file_name='k')
    return response
