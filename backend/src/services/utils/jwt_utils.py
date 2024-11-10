import json
import jwt
import os
from datetime import datetime, timezone, timedelta

def generate_jwt():
    try:
        jwt_token = None
        # print(os.environ["GITHUB_APP_KEYCONTENTS"])
        # with open("../backend/keys/" + os.environ["GITHUB_APP_KEYNAME"], "rb") as fh:
        #     signing_key = fh.read()
            
            
        now = datetime.now(tz=timezone.utc)
        
        jwt_token = jwt.encode(
            {
                "iss": os.environ["GITHUB_CLIENT_ID"],
                "iat": now,
                "exp": now + timedelta(minutes=10),
            },
            os.environ["GITHUB_APP_KEYCONTENTS"],
            algorithm="RS256"
        )
        return jwt_token
    except Exception as e:
        print("e",e)
        return None
