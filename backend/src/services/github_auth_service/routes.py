from fastapi import APIRouter, HTTPException, Header
from typing import Annotated, Any

from src.services.github_auth_service.github_auth_service import github_auth_service

router = APIRouter()


@router.get("/")
def health():
    return {"message": "Auth OK"}


@router.get("/getAccessToken/")
def get_user_token(code: str) -> dict[str, str]:
    try:
        get_token_result = github_auth_service.get_github_auth_token(code)
        return get_token_result

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/getUserInfo")
def get_user_token(
    Authorization: Annotated[str | None, Header()] = None
) -> dict[str, Any]:
    print("Authorization: ", Authorization)
    try:
        user_data = github_auth_service.get_github_user_info(Authorization)
        return user_data

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
