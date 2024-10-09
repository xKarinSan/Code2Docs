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
        print("[get_github_auth_token]", res.json())
        return res.json()

    # used to trigger refresh
    def check_github_app_installations(self, installation_id: str, jwt: str) -> bool:
        headers = {
            "Authorization": "Bearer " + jwt,
            "Accept": "application/vnd.github+json",
        }
        res = get("https://api.github.com/app/installations", headers=headers)

        login_tokens = set()
        for row in res:
            login_tokens.add(res)

        return installation_id in login_tokens

    # takes in installation ID
    def get_github_install_token(self, installation_id: str) -> Dict[str, Any]:
        # installation ID is now Client ID
        installation_token = generate_jwt()
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
        # print("[get_github_install_token]", res.json())
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
            print("[get_github_user_info]", res)
            user_info["username"] = res["login"]
            user_info["displayName"] = res["name"]
            user_info["profilePicUrl"] = res["avatar_url"]
        return user_info

    def get_github_user_repos(
        self, authToken: str, username: str, page_num: int = 1
    ) -> Dict[str, Any]:
        headers = {"Authorization": "Bearer " + authToken}
        res = get(
            f"https://api.github.com/search/repositories?q=user:{username}&page={page_num}"
        )
        res = res.json()
        user_repos_res = {}
        if res.status_code != 200:
            user_repos_res["error"] = True
        else:
            user_repos_res["error"] = False
            user_repos_res["repos"] = res["items"]

        return user_repos_res


github_service = GithubAuthService()
