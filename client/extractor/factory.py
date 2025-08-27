from pydantic import InstanceOf
from client.types import DocumentType
from client.extractor.extractors import SalaryTransactionExtractor
from client.extractor.base import BaseExtractor

class ExtractorFactory:
    def __init__(self):
        self._creators = {}

    def register_document_type(self, document_type: DocumentType, creator: BaseExtractor):
        self._creators[document_type] = creator

    def get_extractor(self, document_type: DocumentType) -> InstanceOf[BaseExtractor]:
        result = self._creators[document_type]
        if not result:
            raise ValueError(document_type)
        return result()

factory = ExtractorFactory()
factory.register_document_type(DocumentType.SALARY_TRANSACTION, SalaryTransactionExtractor)
