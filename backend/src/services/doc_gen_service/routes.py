from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.src.services.doc_gen_service.doc_gen_service import doc_gen_service
from backend.src.services.docs_service.docs_service import docs_service
from backend.src.services.codebase_service.codebase_service import codebase_service

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
def document_zip_file_demo(file: UploadFile) -> dict[str, str]:
    try:
        unzipped_files = doc_gen_service.unzip_file(file.file)
        if not unzipped_files:
            return JSONResponse(
                status_code=400,
                content={"message": "Invalid files"},
            )
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


@router.post("/upload/{user_id}")
def document_zip_file(file: UploadFile, user_id: str) -> dict[str, str]:
    try:
        unzipped_files = doc_gen_service.unzip_file(file.file)
        if not unzipped_files:
            return JSONResponse(
                status_code=400,
                content={"message": "Invalid files"},
            )
        new_codebase = codebase_service.create_codebase(
            {"user_id": user_id, "codebase_name": file.filename}
        )
        if not new_codebase:
            return JSONResponse(
                status_code=500,
                content={"message": "Failed to create new codebase"},
            )
        new_docset = docs_service.create_new_docset(
            {
                "user_id": user_id,
                "codebase_id": new_codebase["codebase_id"],
                "docset_name": file.filename,
            }
        )
        if not new_docset:
            return JSONResponse(
                status_code=500,
                content={"message": "Failed to create new document set"},
            )

        resultant_docs = doc_gen_service.summarise_files(unzipped_files)
        if not resultant_docs:
            return JSONResponse(
                status_code=500,
                content={"message": "Failed to generate documentation"},
            )
        # for each documentation, add 1 doc into the records
        for resultant_doc in resultant_docs:
            docs_service.create_new_doc(
                {
                    "user_id": user_id,
                    "docset_id": new_docset["docset_id"],
                    "doc_name": resultant_doc["file_name"],
                    "contents": resultant_doc["contents"],
                }
            )

        return JSONResponse(status_code=200, content=resultant_docs)

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
