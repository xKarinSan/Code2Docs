import os
from typing import Any, Dict
from requests import get, post

from dotenv import load_dotenv, find_dotenv
from backend.src.services.utils.jwt_utils import generate_jwt


class GithubService:
    def __init__(self):
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
        res = res.json()
        return res

    # used to trigger refresh
    def check_github_app_installations(self, jwt: str) -> bool:
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
        print("installation_id", installation_id)
        # installation ID is now Client ID
        generated_jwt = generate_jwt()
        print("generated_jwt", generated_jwt)

        res = post(
            f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {generated_jwt}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        res = res.json()
        return {"token": res["token"], "bearer_token": generated_jwt}

    def get_github_install_status(self, username: str) -> int:
        if not username:
            return False
        # call the API endpoint:  https://api.github.com/users/{username}/installation
        # just add the jwt as the bearer token
        generated_jwt = generate_jwt()

        res = get(
            f"https://api.github.com/app/installations",
            headers={
                "Authorization": f"Bearer {generated_jwt}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        res = res.json()
        download_users = {}
        for installation in res:
            download_users[installation["account"]["login"]] = installation["id"]

        return download_users[username] if username in download_users else -1

    """
    Gets the basic info of an authenticated user
    """

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
            user_info["username"] = res["login"]
            user_info["displayName"] = res["name"]
            user_info["profilePicUrl"] = res["avatar_url"]
        return user_info

    """
    Gets the repos of an authenticated user
    """

    def get_github_user_repos(
        self, authToken: str, username: str, page_num: int = 1, per_page: int = 30
    ) -> Dict[str, Any]:
        try:
            if per_page < 1:
                per_page = 30
            if per_page > 100:
                per_page = 100
            headers = {
                "Authorization": authToken,
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
            res = get(
                f"https://api.github.com/search/repositories?q=user:{username}&page={page_num}&per_page={per_page}",
                headers=headers,
            )
            user_repos_res = {}
            if res.status_code != 200:
                user_repos_res["error"] = True
            else:
                res = res.json()
                extra_page = 1 if res["total_count"] % page_num != 0 else 0

                user_repos_res["error"] = False
                user_repos_res["repos"] = res["items"]
                user_repos_res["pages_count"] = (
                    res["total_count"] // per_page
                ) + extra_page

            return user_repos_res
        except Exception as e:
            user_repos_res["error"] = True
            return user_repos_res

    def get_user_repo_in_zip(self, authToken: str, username: str, reponame: str):
        headers = {
            "Authorization": authToken,
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        res = get(
            f"https://api.github.com/repos/{username}/{reponame}/zipball",
            headers=headers,
            stream=True,
        )
        res.headers["Content-Type"] = "application/zip"
        res.headers["Content-Disposition"] = f"attachment; filename=${reponame}.zip"
        print('res:',res.headers)
        print('res:',res.content)

        # return res
        for chunk in res.iter_content(chunk_size=8192):  # Adjust chunk size as needed
            yield chunk


load_dotenv(find_dotenv())
github_service = GithubService()
