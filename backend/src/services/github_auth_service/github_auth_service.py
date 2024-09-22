import os
from typing import Any, Dict
from requests import get, post

from dotenv import load_dotenv, find_dotenv
from src.services.utils.jwt_utils import generate_jwt

class GithubAuthService:
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        self.github_client_id = os.environ["GITHUB_CLIENT_ID"]
        self.github_client_secret = os.environ["GITHUB_CLIENT_SECRET"]

    def get_github_auth_token(self, code: str) -> Dict[str, str] | None:
        params = (
            "?client_id="
            + self.github_client_id
            + "&client_secret="
            + self.github_client_secret
            + "&code="
            + code
        )
        headers = {
            "Accept": "application/vnd.github+json",
        }
        res = post(
            "https://github.com/login/oauth/access_token" + params, headers=headers
        )
        print(res.json())
        return res.json()
    
    def get_github_install_token(self, installation_id: str) -> Dict[str, Any]:
        # installation ID is now Client ID
        installation_token = generate_jwt()
        print("code:", installation_id)
        # print("self.github_installation_id :", self.github_installation_id)
        print("installation_token: ", installation_token)
        headers = {
            "Authorization": "Bearer " + installation_token,
            "Accept": "application/vnd.github+json",
        }

        res = post(
            f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {installation_token}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        print("[get_github_install_token] res:", res.json())
        return {"token": res.json()["token"], "bearer_token": installation_token}

    def get_github_user_info(self, authToken: str) -> Dict[str, Any] | None:
        # authorisation -> bearer token
        headers = {"Authorization": "Bearer " + authToken}
        res = get("https://api.github.com/user", headers=headers)
        user_info = {}
        if res.status_code != 200:
            user_info["error"] = True
        else:
            user_info["error"] = False
            res = res.json()
            user_info["username"] = res["name"]
            user_info["profilePic"] = res["avatar_url"]
        return user_info


github_auth_service = GithubAuthService()
