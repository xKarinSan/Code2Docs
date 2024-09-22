from fastapi import APIRouter, HTTPException, Header, status
from fastapi.responses import RedirectResponse

from typing import Annotated, Any

from src.services.github_auth_service.github_auth_service import github_auth_service

router = APIRouter()


@router.get("/")
def health():
    return {"message": "Auth OK"}


@router.get("/getAccessToken/")
def get_user_token(code: str) -> dict[str, Any]:
    try:
        get_token_result = github_auth_service.get_github_auth_token(code)
        if "access_token" in get_token_result:
            return {"access_token": get_token_result["access_token"]}

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/installationToken/")
def get_user_installation(installation_id: str) -> dict[str, Any]:
    try:

        get_token_result = github_auth_service.get_github_install_token(installation_id)
        return {"token": get_token_result["token"]}
    
    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/getUserInfo")
def get_user_token(
    Authorization: Annotated[str | None, Header()] = None
) -> dict[str, Any]:
    try:
        user_data = github_auth_service.get_github_user_info(Authorization)
        # print("user_data",user_data)
        if "access_token" in user_data:
            # access auth
            return
        return user_data

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
