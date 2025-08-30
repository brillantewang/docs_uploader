from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from client import Classifier, Extractor, Storage, GoogleDrive
from global_types import DocumentType

app = FastAPI()

class GDriveParts(BaseModel):
    document_type: str
    output_file_name: str

@app.post('/documents/g_drive_parts')
async def create_g_drive_parts(document: UploadFile) -> GDriveParts:
    # Uploads document to GCS
    Storage().upload(file_name=document.filename, file=document.file, content_type=document.content_type)

    # Hits classifier processor to get document type
    document_type = await Classifier().get_document_type(document)

    # It chooses the right extractor based on the document_type
    extractor = Extractor(document_type)

    # It constructs the g_drive_file_name based on the document contents
    output_file_name = await extractor.get_g_drive_file_name(document)

    # Returns the document_type and g_drive_file_name
    response = GDriveParts(document_type=document_type, output_file_name=output_file_name)
    return response

class DocumentSubmitBody(BaseModel):
    gcs_file_name: str
    document_type: DocumentType # this should be provided to client from /documents/g_drive_parts, or client can edit it
    output_file_name: str # this should be provided to client from /documents/g_drive_parts, or client can edit it

class DocumentSubmitResponse(BaseModel):
    g_drive_file_id: str

@app.post('/documents/submit')
async def upload_to_g_drive(body: DocumentSubmitBody):
    with Storage().open(body.gcs_file_name) as gcs_file:
        response = GoogleDrive().upload_file(
            file=gcs_file,
            output_file_name=body.output_file_name,
            document_type=body.document_type,
        )
    return DocumentSubmitResponse(g_drive_file_id=response['id'])
