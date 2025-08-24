from fastapi import File

class Storage:
    def __init__(self):
        pass

    def upload(self, file_name: str, file: File):
        print('uploading ', file_name)
