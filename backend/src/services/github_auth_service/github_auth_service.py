import os
from typing import Any, Dict
from requests import get, post

from dotenv import load_dotenv, find_dotenv


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
        return res.json()

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
