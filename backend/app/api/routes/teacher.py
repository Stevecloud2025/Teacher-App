from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.teacher import (
    TeacherCreate,
    TeacherLogin,
    TeacherResponse,
    LoginResponse,
    TeacherProfileResponse
)

from app.schemas.teacher import (
    TeacherCreate,
    TeacherLogin,
    TeacherResponse,
    LoginResponse,
    TeacherProfileResponse,
    TeacherProfileUpdate
)

from app.schemas.teacher import (
    TeacherCreate,
    TeacherLogin,
    TeacherResponse,
    LoginResponse,
    TeacherProfileResponse,
    TeacherProfileUpdate,
    ChangePasswordRequest
)
from app.database.database import get_db
from app.models.teacher import Teacher

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.api.dependencies import get_current_teacher



router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)


@router.post("/register", response_model=TeacherResponse)
def register_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db)
):
    existing_teacher = db.query(Teacher).filter(
        Teacher.email == teacher.email
    ).first()

    if existing_teacher:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_teacher = Teacher(
        full_name=teacher.full_name,
        email=teacher.email,
        phone=teacher.phone,
        password=hash_password(teacher.password),
        school_name=teacher.school_name
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return {
        "id": new_teacher.id,
        "full_name": new_teacher.full_name,
        "email": new_teacher.email,
        "phone": new_teacher.phone,
        "school_name": new_teacher.school_name
    }


@router.post("/login", response_model=LoginResponse)
def login_teacher(
    teacher: TeacherLogin,
    db: Session = Depends(get_db)

    
):
    # Find teacher by email
    db_teacher = db.query(Teacher).filter(
        Teacher.email == teacher.email
    ).first()

    # Check if teacher exists
    if not db_teacher:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check password
    if not verify_password(
        teacher.password,
        db_teacher.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT access token
    access_token = create_access_token(
        {"sub": str(db_teacher.id)}
    )

    return {
        "message": "Login successful",
        "teacher_id": db_teacher.id,
        "full_name": db_teacher.full_name,
        "email": db_teacher.email,
        "access_token": access_token
    }

@router.get("/me", response_model=TeacherResponse)
def get_my_profile(
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    db_teacher = db.query(Teacher).filter(
        Teacher.id == int(teacher_id)
    ).first()

    if not db_teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return {
        "id": db_teacher.id,
        "full_name": db_teacher.full_name,
        "email": db_teacher.email,
        "phone": db_teacher.phone,
        "school_name": db_teacher.school_name
    }
@router.get("/profile", response_model=TeacherProfileResponse)
def get_teacher_profile(
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == int(teacher_id)
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher

@router.put("/profile", response_model=TeacherProfileResponse)
def update_teacher_profile(
    profile: TeacherProfileUpdate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == int(teacher_id)
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    teacher.full_name = profile.full_name
    teacher.phone = profile.phone
    teacher.school_name = profile.school_name

    db.commit()
    db.refresh(teacher)

    return teacher

@router.put("/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == int(teacher_id)
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    if not verify_password(
        password_data.current_password,
        teacher.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    teacher.password = hash_password(
        password_data.new_password
    )

    db.commit()

    return {
        "message": "Password changed successfully"
    }