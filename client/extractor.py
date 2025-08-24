from fastapi import File

class Extractor:
    def __init__(self, document_type: str):
        pass

    def get_g_drive_file_name(self, document: File) -> str:
        return 'g drive file name'
