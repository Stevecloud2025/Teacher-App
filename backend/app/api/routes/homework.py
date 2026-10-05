from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.homework import Homework
from app.schemas.homework import HomeworkCreate, HomeworkResponse
from app.api.dependencies import (
    get_current_teacher,
    get_current_student
)


router = APIRouter(
    prefix="/homework",
    tags=["Homework"]
)


@router.post("/", response_model=HomeworkResponse)
def create_homework(
    homework: HomeworkCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    new_homework = Homework(
        title=homework.title,
        description=homework.description,
        subject=homework.subject,
        class_name=homework.class_name,
        due_date=homework.due_date,
        teacher_id=teacher_id
    )

    db.add(new_homework)
    db.commit()
    db.refresh(new_homework)

    return new_homework


@router.get("/", response_model=list[HomeworkResponse])
def get_homework(
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    return db.query(Homework).filter(
        Homework.teacher_id == teacher_id
    ).order_by(
        Homework.due_date.asc()
    ).all()

@router.get(
    "/student",
    response_model=list[HomeworkResponse]
)
def get_student_homework(
    student_id: str = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    return db.query(Homework).order_by(
        Homework.due_date.asc()
    ).all()


@router.get("/{homework_id}", response_model=HomeworkResponse)
def get_homework_by_id(
    homework_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    homework = db.query(Homework).filter(
        Homework.id == homework_id,
        Homework.teacher_id == teacher_id
    ).first()

    if not homework:
        raise HTTPException(
            status_code=404,
            detail="Homework not found"
        )

    return homework


@router.put("/{homework_id}", response_model=HomeworkResponse)
def update_homework(
    homework_id: int,
    homework: HomeworkCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    existing_homework = db.query(Homework).filter(
        Homework.id == homework_id,
        Homework.teacher_id == teacher_id
    ).first()

    if not existing_homework:
        raise HTTPException(
            status_code=404,
            detail="Homework not found"
        )

    existing_homework.title = homework.title
    existing_homework.description = homework.description
    existing_homework.subject = homework.subject
    existing_homework.class_name = homework.class_name
    existing_homework.due_date = homework.due_date

    db.commit()
    db.refresh(existing_homework)

    return existing_homework


@router.delete("/{homework_id}")
def delete_homework(
    homework_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    homework = db.query(Homework).filter(
        Homework.id == homework_id,
        Homework.teacher_id == teacher_id
    ).first()

    if not homework:
        raise HTTPException(
            status_code=404,
            detail="Homework not found"
        )

    db.delete(homework)
    db.commit()

    return {
        "message": "Homework deleted successfully"
    }


