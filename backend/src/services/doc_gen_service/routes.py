from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.src.services.doc_gen_service.doc_gen_service import doc_gen_service

from backend.src.services.docs_service.schemas.DocSetSchemas import (
    DocSet,
    CreateDocSet,
)
import logging

router = APIRouter()


@router.get("/")
def health():
    return {"message": "OK"}


"""
To be changed
"""


@router.post("/")
def document_zip_file(file: UploadFile) -> dict[str, str]:
    try:
        unzipped_files = doc_gen_service.unzip_file(file.file)
        if not unzipped_files:
            return JSONResponse(
                status_code=400,
                content={"message": "Invalid files"},
            )
        logging.info("unzipped_files", unzipped_files)
        documentation_string = doc_gen_service.summarise_files_demo(unzipped_files)
        if not documentation_string:
            return JSONResponse(
                status_code=500,
                content={"message": "Failed to generate documentation"},
            )
        return JSONResponse(status_code=200, content={"data": documentation_string})

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


