import os
from typing import Dict
from requests import post

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
        headers = {"Accept": "application/json"}
        res = post(
            "https://github.com/login/oauth/access_token" + params, headers=headers
        )
        return res.json()


github_auth_service = GithubAuthService()
