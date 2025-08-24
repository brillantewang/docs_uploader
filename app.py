from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Document(BaseModel):
    document: bytes
    source_file_name: str

class GDriveParts(BaseModel):
    document_type: str
    g_drive_file_name: str

@app.post('/documents/g_drive_parts')
async def create_g_drive_parts(document: Document) -> GDriveParts:
    response = GDriveParts(document_type='dog', g_drive_file_name='k')
    return response
