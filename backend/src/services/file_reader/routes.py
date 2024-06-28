from fastapi import APIRouter, UploadFile
from services.file_reader.file_reader import file_reader

router = APIRouter()


@router.post("/")
def upload_zip_file(file: UploadFile):
    print("file", file)
    file_reader.unzip_file(file.file)
    return {"message": "uploaded"}