from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from client import Classifier, Extractor, Storage

app = FastAPI()

class GDriveParts(BaseModel):
    document_type: str
    g_drive_file_name: str

@app.post('/documents/g_drive_parts')
async def create_g_drive_parts(document: UploadFile) -> GDriveParts:
    # Uploads document to GCS
    Storage().upload(file_name=document.filename, file=document)

    # Hits classifier processor to get document type
    document_type = Classifier().get_document_type()

    # It chooses the right extractor based on the document_type
    extractor = Extractor(document_type)

    # It constructs the g_drive_file_name based on the document contents
    g_drive_file_name = extractor.get_g_drive_file_name(document)

    # Returns the document_type and g_drive_file_name
    response = GDriveParts(document_type=document_type, g_drive_file_name=g_drive_file_name)
    return response
