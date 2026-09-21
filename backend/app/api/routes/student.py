from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.student import Student
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentLogin
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.api.dependencies import get_current_student

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

@router.post("/login")
def login_student(
    student: StudentLogin,
    db: Session = Depends(get_db)
):
    db_student = db.query(Student).filter(
        Student.email == student.email
    ).first()

    if not db_student:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        student.password,
        db_student.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(db_student.id),
            "role": "student"
        }
    )

    return {
        "message": "Login successful",
        "student_id": db_student.id,
        "full_name": db_student.full_name,
        "email": db_student.email,
        "access_token": access_token
    }

@router.get("/me", response_model=StudentResponse)
def get_my_student_profile(
    student_id: str = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == int(student_id)
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student