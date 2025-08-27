from pydantic import InstanceOf
from client.types import DocumentType
from client.extractor.factory import factory
from client.extractor.base import BaseExtractor
from fastapi import UploadFile

class Extractor:
    def __init__(self, document_type: DocumentType):
        self.extractor: InstanceOf[BaseExtractor] = factory.get_extractor(document_type)

    async def get_g_drive_file_name(self, document: UploadFile) -> str:
        return await self.extractor.get_g_drive_file_name(document)
