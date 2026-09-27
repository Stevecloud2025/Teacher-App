from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_access_token


security = HTTPBearer()


def get_current_teacher(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if payload.get("role") != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required"
        )

    teacher_id = payload.get("sub")

    if teacher_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid teacher token"
        )

    return teacher_id

def get_current_student(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if payload.get("role") != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access required"
        )

    student_id = payload.get("sub")

    if student_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid student token"
        )

    return student_id