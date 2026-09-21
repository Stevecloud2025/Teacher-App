from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse
from app.core.security import hash_password


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post(
    "/register",
    response_model=StudentResponse
)
def register_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = db.query(Student).filter(
        Student.email == student.email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="A student with this email already exists"
        )

    hashed_password = hash_password(student.password)

    new_student = Student(
        full_name=student.full_name,
        email=student.email,
        password=hashed_password,
        school_name=student.school_name,
        class_name=student.class_name
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student