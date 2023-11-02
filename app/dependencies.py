import os
import jwt
import logging
from typing import Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from internal.token_handler import is_valid_token, is_valid_email
from internal.token_handler import EMAIL_KEY, USER_TYPE_KEY

security = HTTPBearer()

async def get_current_email_type(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Tuple[str, str]:
    token = credentials.credentials

    if not is_valid_token(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = jwt.decode(token, options={"verify_signature": False})
    if not is_valid_email(payload[EMAIL_KEY]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find email",
        )

    return payload[EMAIL_KEY], payload[USER_TYPE_KEY]


jwt_dependency = Depends(get_current_email_type)
