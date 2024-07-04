from fastapi import APIRouter, UploadFile
from services.file_reader.file_reader import file_reader
from services.document_serivice.document_service import document_service

router = APIRouter()


@router.post("/")
def upload_zip_file(file: UploadFile):
    document_service.unzip_file(file.file)
    return {"message": "uploaded"}
