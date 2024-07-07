from fastapi import APIRouter, UploadFile
from services.document_service.document_service import document_service

router = APIRouter()

@router.post("/")
def document_zip_file(file: UploadFile):
    try:
        unzipped_files = document_service.unzip_file(file.file)
        res = document_service.summarise_files(unzipped_files)
        return {"data": res}
    
    except Exception as e:
        return {"error": e}
