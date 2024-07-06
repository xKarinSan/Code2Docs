from fastapi import APIRouter, UploadFile
from services.file_reader.file_reader import file_reader
from services.document_service.document_service import document_service

router = APIRouter()


@router.post("/")
def summarise_zip_file(file: UploadFile):
    try:
        document_service.unzip_file(file.file)
        res = document_service.summarise_files()
        return {"data": res}

    except Exception as e:
        return {"error": e}
