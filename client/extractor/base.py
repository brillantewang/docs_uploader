from abc import ABC, abstractmethod
from fastapi import UploadFile

class BaseExtractor(ABC):
    """Abstract base class for all extractors"""

    @abstractmethod
    async def get_g_drive_file_name(self, document: UploadFile) -> str:
        """
        Extract and return the Google Drive file name for the document.

        Args:
            document: The uploaded document file

        Returns:
            str: The formatted Google Drive file name
        """
        pass
