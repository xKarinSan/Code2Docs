from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from src.services.document_service.document_service import document_service

router = APIRouter()


@router.post("/")
async def document_zip_file(file: UploadFile) -> dict[str, str]:
    try:
        unzipped_files = await document_service.unzip_file(file.file)
        if not unzipped_files:
            return JSONResponse(
                status_code=400,
                content={"message": "Invalid files"},
            )
        documentation_string = await document_service.summarise_files(unzipped_files)
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
