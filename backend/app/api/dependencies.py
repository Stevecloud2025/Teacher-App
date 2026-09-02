from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_access_token


security = HTTPBearer()


def get_current_teacher(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    teacher_id = verify_access_token(token)

    if teacher_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return teacher_id