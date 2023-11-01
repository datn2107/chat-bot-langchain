import os
import jwt

def generate_external_server_token() -> str:
    token = jwt.encode(
        {}, os.environ.get("JWT_SECRET"), algorithm=os.environ.get("JWT_ALGORITHM")
    )
    return token

def is_valid_token(token: str) -> bool:
    try:
        jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=[os.environ.get("JWT_ALGORITHM")])
        return True
    except:
        return False
