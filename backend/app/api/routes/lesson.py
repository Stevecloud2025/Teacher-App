from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.lesson import Lesson
from app.schemas.lesson import (
    LessonCreate,
    LessonResponse,
    LessonListResponse
)
from app.api.dependencies import get_current_teacher


router = APIRouter(
    prefix="/lessons",
    tags=["Lessons"]
)


@router.post("/", response_model=LessonResponse)
def create_lesson(
    lesson: LessonCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    new_lesson = Lesson(
    title=lesson.title,
    subject=lesson.subject,
    class_name=lesson.class_name,
    topic=lesson.topic,
    content=lesson.content,
    status=lesson.status,
    teacher_id=int(teacher_id)
)

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson


@router.get("/", response_model=LessonListResponse)
def get_lessons(
    subject: str | None = None,
    class_name: str | None = None,
    topic: str | None = None,
    search: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    query = db.query(Lesson).filter(
        Lesson.teacher_id == int(teacher_id)
    )

    if subject:
        query = query.filter(
            Lesson.subject == subject
        )

    if class_name:
        query = query.filter(
            Lesson.class_name == class_name
        )

    if topic:
        query = query.filter(
            Lesson.topic == topic
        )

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            Lesson.title.ilike(search_term) |
            Lesson.subject.ilike(search_term) |
            Lesson.topic.ilike(search_term) |
            Lesson.content.ilike(search_term)
        )

    if status:
        if status not in ["draft", "published", "archived"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid status. Use draft, published, or archived."
            )

        query = query.filter(
            Lesson.status == status
        )

    total_lessons = query.count()

    offset = (page - 1) * limit

    lessons = query.order_by(
        Lesson.created_at.desc()
    ).offset(offset).limit(limit).all()

    total_pages = (total_lessons + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total_lessons,
        "total_pages": total_pages,
        "lessons": lessons
    }


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.teacher_id == int(teacher_id)
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return lesson

@router.post("/{lesson_id}/duplicate", response_model=LessonResponse)
def duplicate_lesson(
    lesson_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    original_lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.teacher_id == int(teacher_id)
    ).first()

    if not original_lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    duplicated_lesson = Lesson(
    title=f"{original_lesson.title} - Copy",
    subject=original_lesson.subject,
    class_name=original_lesson.class_name,
    topic=original_lesson.topic,
    content=original_lesson.content,
    status="draft",
    teacher_id=int(teacher_id)
)

    db.add(duplicated_lesson)
    db.commit()
    db.refresh(duplicated_lesson)

    return duplicated_lesson

@router.patch("/{lesson_id}/status", response_model=LessonResponse)
def update_lesson_status(
    lesson_id: int,
    status: str,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    if status not in ["draft", "published", "archived"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Use draft, published, or archived."
        )

    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.teacher_id == int(teacher_id)
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    lesson.status = status

    db.commit()
    db.refresh(lesson)

    return lesson


@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson: LessonCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    existing_lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.teacher_id == int(teacher_id)
    ).first()

    if not existing_lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    existing_lesson.title = lesson.title
    existing_lesson.subject = lesson.subject
    existing_lesson.class_name = lesson.class_name
    existing_lesson.topic = lesson.topic
    existing_lesson.content = lesson.content

    db.commit()
    db.refresh(existing_lesson)

    return existing_lesson


@router.delete("/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.teacher_id == int(teacher_id)
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    db.delete(lesson)
    db.commit()

    return {
        "message": "Lesson deleted successfully"
    }