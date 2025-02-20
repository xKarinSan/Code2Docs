from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.services.docs_service.schemas.DocSetSchemas import CreateDocSet, DocSet

from src.services.docs_service.schemas.DocSchemas import Docs, CreateDocs

from src.services.docs_service.docs_service import docs_service

router = APIRouter()


# ================ for document sets ================
@router.post("/set")
def upload_doc_set(new_docset: CreateDocSet) -> dict[str, DocSet]:
    try:
        uploaded_doc = docs_service.create_new_docset(new_docset.model_dump())
        return JSONResponse(status_code=200, content=uploaded_doc)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/set/{docset_id}/u/{user_id}")
def get_docset_by_id(docset_id: int, user_id: str):
    try:
        current_docset = docs_service.get_docset_by_id(docset_id, user_id)
        return JSONResponse(status_code=200, content=current_docset)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/set/u/{user_id}")
def get_user_docsets(user_id: str):
    try:
        current_docset = docs_service.get_user_docsets(user_id)
        return JSONResponse(status_code=200, content=current_docset)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/set/c/{codebase_id}/u/{user_id}")
def get_docsets_in_codebase(codebase_id: int, user_id: str):
    try:
        docsets_in_codebase = docs_service.get_docsets_in_codebase(codebase_id, user_id)
        return JSONResponse(status_code=200, content=docsets_in_codebase)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================ for documents themselves ================
@router.post("/")
def upload_doc(new_docs: CreateDocs):
    try:
        uploaded_doc = docs_service.create_new_doc(new_docs.model_dump())
        return JSONResponse(status_code=200, content=uploaded_doc)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/s/{docset_id}/u/{user_id}")
def get_docs_from_docset(docset_id: int, user_id: str):
    try:
        authorised_docs = docs_service.get_docs_from_docset(docset_id, user_id)
        print("authorised_docs", authorised_docs)
        return JSONResponse(status_code=200, content=authorised_docs)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{doc_id}/u/{user_id}")
def get_docs_by_id(doc_id: int, user_id: str):
    try:
        current_doc = docs_service.get_docs_by_id(doc_id, user_id)
        return JSONResponse(status_code=200, content=current_doc)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/u/{user_id}")
def get_docs_by_id(user_id: str):
    try:
        current_doc = docs_service.get_docs_by_user(user_id)
        return JSONResponse(status_code=200, content=current_doc)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
