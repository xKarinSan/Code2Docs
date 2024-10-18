from fastapi import APIRouter, HTTPException, Header, status, Response
from fastapi.responses import RedirectResponse, JSONResponse

from typing import Annotated, Any

from src.services.github_service.github_service import github_service
from src.services.utils.jwt_utils import generate_jwt

router = APIRouter()


@router.get("/")
def health():
    return {"message": "Auth OK"}


@router.get("/login/")
def get_user_login(code: str, response: Response) -> dict[str, Any]:
    try:
        print("[GET] /login/")
        get_token_result = github_service.get_github_auth_token(code)
        response.set_cookie(
            key="code2docs_auth_refresh_token", value=get_token_result["refresh_token"]
        )
        if "access_token" in get_token_result and "refresh_token" in get_token_result:
            jwt = generate_jwt()
            user_info = github_service.get_github_user_info(
                get_token_result["access_token"]
            )

            return {
                "username": user_info["username"],
                "display_name": user_info["displayName"],
                "profile_pic_url": user_info["profilePicUrl"],
                "access_token": get_token_result["access_token"],
                "refresh_token": get_token_result["refresh_token"],
                "app_install_jwt": jwt,
            }

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/install/")
def get_user_installation(installation_id: str) -> dict[str, Any]:
    try:
        print("[GET] /install/")
        get_token_result = github_service.get_github_install_token(installation_id)
        print("get_token_result", get_token_result)
        return {"token": get_token_result["token"]}

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/install/check/{username}")
def get_user_installation(username: str) -> dict[str, Any]:
    try:
        print("[GET] /install/check/{username}")
        get_installation_result = github_service.get_github_install_status(username)
        return {"installation_id": get_installation_result}

    except HTTPException as he:
        # Re-raise HTTPExceptions as they already have status codes
        raise he

    except Exception as e:
        print(e)
        return {"installation_id": None}


@router.get("/repos/u/{username}")
def get_user_repositories(
    username: str,
    Authorization: Annotated[str | None, Header()] = None,
    page_num: int = 1,
    per_page: int = 30,
) -> dict[str, Any]:
    try:
        get_repository_result = github_service.get_github_user_repos(
            Authorization, username, page_num, per_page
        )
        return get_repository_result

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.get("/getUserInfo")
# def get_user_login(
#     Authorization: Annotated[str | None, Header()] = None
# ) -> dict[str, Any]:
#     try:
#         user_data = github_service.get_github_user_info(Authorization)
#         if "access_token" in user_data:
#             return
#         return user_data

#     except HTTPException as he:
#         # Re-raise HTTPExceptions as they already have status codes
#         raise he

#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail=str(e))
