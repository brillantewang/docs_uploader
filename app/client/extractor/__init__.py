from pydantic import InstanceOf
from app.global_types import DocumentType
from app.client.extractor.factory import factory
from app.client.extractor.extractors import BaseExtractor
from fastapi import UploadFile

class Extractor:
    def __init__(self, document_type: DocumentType):
        self.extractor: InstanceOf[BaseExtractor] = factory.get_extractor(document_type)

    async def get_g_drive_file_name(self, document: UploadFile) -> str:
        return await self.extractor.get_g_drive_file_name(document)
