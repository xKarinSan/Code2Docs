from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.src.services.codebase_service.CodebaseSchemas import (
    CreateCodebase,
    Codebase,
)
from backend.src.services.codebase_service.codebase_service import codebase_service
from typing import Any

router = APIRouter()


@router.post("/")
def create_codebase_route(codebase: CreateCodebase) -> dict[str, Codebase]:
    try:
        created_codebase = codebase_service.create_codebase(codebase.model_dump())
        if created_codebase == None:
            return JSONResponse(
                status_code=500, content={"message": "Failed to create codebase"}
            )
        return JSONResponse(status_code=201, content=created_codebase)
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
def get_all_codebases() -> dict[str, list[Codebase]]:
    try:
        all_codebases = codebase_service.get_all_codebases()
        return JSONResponse(status_code=200, content=all_codebases)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/u/{userId}")
def get_user_codebases(userId: str) -> dict[str, Any]:
    try:
        all_codebases = codebase_service.get_all_user_codebases(userId)
        return JSONResponse(status_code=200, content=all_codebases)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/id/{codebaseId}/{userId}")
def get_codebase_by_id(codebaseId: int, userId: str) -> dict[str, Any]:
    try:
        current_codebase = codebase_service.get_codebase_by_id(codebaseId, userId)
        return JSONResponse(status_code=200, content=current_codebase)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
