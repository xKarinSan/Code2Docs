from typing import BinaryIO
from zipfile import ZipFile
from fastapi import UploadFile
from io import BytesIO


class FileHandlerService:
    
    def unzip_file(self, file: BinaryIO) -> None:
        read_zip_file = ZipFile(BytesIO(file.read()))
        print("read_zip_file", read_zip_file)
        print("read_zip_file.namelist", read_zip_file.namelist())
        read_zip_file.extractall("../file_items", read_zip_file.namelist())


file_handler_service = FileHandlerService()
