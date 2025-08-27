from fastapi import UploadFile
from google.cloud.documentai import DocumentProcessorServiceAsyncClient, RawDocument, ProcessRequest
from config import config
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Literal
from client.extractor.base import BaseExtractor
import calendar
import re

class EntityModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type_: Literal['transfer_date', 'salary_month']

class DateTimeValueModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    year: int
    month: int
    day: int

class NormalizedValueModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    datetime_value: DateTimeValueModel

class TransferDateEntityModel(EntityModel):
    normalized_value: NormalizedValueModel

class SalaryMonthEntityModel(EntityModel):
    mention_text: str

class DocumentModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    entities: Annotated[list[EntityModel], Field(min_length=2)]

class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    document: DocumentModel

class SalaryTransactionExtractor(BaseExtractor):
    def __init__(self):
        self.client = DocumentProcessorServiceAsyncClient()
        self.process_id = config.MA_SALARY_TRANSACTION_EXTRACTOR_PROCESSOR_ID

    def _get_salary_month(self, entities: Annotated[list[EntityModel], Field(min_length=2)]) -> str:
        salary_month: SalaryMonthEntityModel = next(entity for entity in entities if entity.type_ == 'salary_month')
        SalaryMonthEntityModel.model_validate(salary_month)

        # Validate the salary month format
        # Must be like '5月' or just '5'
        pattern = r'^(\d+)(?:月)?$'
        match = re.match(pattern, salary_month.mention_text)

        if not match:
            raise ValueError(f"Invalid salary month format: {salary_month.mention_text}. Expected format: '5月' or '5'")

        month_number = int(match.group(1))

        if month_number < 1 or month_number > 12:
            raise ValueError(f"Invalid month number: {month_number}. Month must be between 1 and 12")

        # Return the month name
        return calendar.month_abbr[month_number]

    def _get_transfer_date(self, entities: Annotated[list[EntityModel], Field(min_length=2)]) -> str:
        transfer_date: TransferDateEntityModel = next(entity for entity in entities if entity.type_ == 'transfer_date')
        TransferDateEntityModel.model_validate(transfer_date)

        date = transfer_date.normalized_value.datetime_value
        return f'{date.year}-{date.month:02}-{date.day:02}'

    # [TransferDate]_Lilis[Month]SalaryTransaction
    async def get_g_drive_file_name(self, document: UploadFile) -> str:
        # Read the file content
        await document.seek(0) # Reset file position so it can be read
        content = await document.read()

        raw_document = RawDocument(
            content=content,
            mime_type=document.content_type
        )

        processor_name = self.client.processor_path(config.PROJECT_ID, config.LOCATION, self.process_id)
        request = ProcessRequest(
            name=processor_name,
            raw_document=raw_document
        )

        response = await self.client.process_document(request=request)
        ResponseModel.model_validate(response)

        transfer_date = self._get_transfer_date(response.document.entities)
        salary_month = self._get_salary_month(response.document.entities)
        return f'{transfer_date}_Lilis{salary_month}SalaryTransaction'
