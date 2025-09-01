from fastapi import UploadFile
from google.cloud.documentai import DocumentProcessorServiceAsyncClient, ProcessRequest, RawDocument
from app.config import config
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from app.global_types import DocumentType

class EntityModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type_: DocumentType

class DocumentModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    entities: Annotated[list[EntityModel], Field(min_length=1)]

class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    document: DocumentModel

class Classifier:
    def __init__(self):
        self.client = DocumentProcessorServiceAsyncClient()
        self.processor_id = config.MA_DOCS_CLASSIFIER_PROCESSOR_ID

    async def get_document_type(self, document: UploadFile) -> str:
        # Read the file content
        await document.seek(0) # Reset file position so it can be read
        content = await document.read()

        raw_document = RawDocument(
            content=content,
            mime_type=document.content_type
        )

        processor_name = self.client.processor_path(config.DOCS_UPLOADER_PROJECT_ID, config.LOCATION, self.processor_id)
        request = ProcessRequest(
            name=processor_name,
            raw_document=raw_document
        )

        response = await self.client.process_document(request=request)
        ResponseModel.model_validate(response)
        return response.document.entities[0].type_
