from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.src.services.docs_service.schemas.DocSetSchemas import CreateDocSet, DocSet
from backend.src.services.docs_service.docs_service import docs_service

router = APIRouter()


@router.post("/set")
def upload_doc_set(new_docset: CreateDocSet) -> dict[str, DocSet]:
    try:
        uploaded_doc = docs_service.create_new_document_set(new_docset.model_dump())
        return JSONResponse(status_code=200, content=uploaded_doc)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
