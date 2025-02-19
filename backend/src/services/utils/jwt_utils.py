import json
import jwt
import os
from datetime import datetime, timezone, timedelta
import boto3

def generate_jwt():
    try:
        jwt_token = None
        get_secret_value_response = boto_client.get_secret_value(
            SecretId=os.environ["BOTO_SECRET_NAME"]
        )
        secret_string = get_secret_value_response["SecretString"]

        secret_json = json.loads(secret_string, strict=False)
        now = datetime.now(tz=timezone.utc)

        jwt_token = jwt.encode(
            {
                "iss": os.environ["GITHUB_CLIENT_ID"],
                "iat": now,
                "exp": now + timedelta(minutes=10),
            },
            secret_json[os.environ["BOTO_SECRET_KEYNAME"]],
            algorithm="RS256",
        )
        return jwt_token
    except Exception as e:
        print("e", e)
        return None


def get_session_client():
    # region_name = "ap-southeast-1"
    session = boto3.session.Session()
    boto_client = session.client(
        service_name="secretsmanager", region_name=os.environ["BOTO_REGION_NAME"]
    )
    return boto_client

boto_client = get_session_client()
