from pydantic import InstanceOf
from app.global_types import DocumentType
from app.client.extractor.extractors import BaseExtractor, SalaryTransactionExtractor

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
