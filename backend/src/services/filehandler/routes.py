from fastapi import APIRouter, UploadFile
from services.filehandler.filehandler import file_handler_service

router = APIRouter()


@router.post("/")
def upload_zip_file(file: UploadFile):
    print("file", file)
    file_handler_service.unzip_file(file.file)
    return {"message": "uploaded"}
