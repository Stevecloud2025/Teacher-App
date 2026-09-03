from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.database import get_db
from app.models.lesson import Lesson
from app.models.teacher import Teacher
from app.api.dependencies import get_current_teacher
from app.schemas.dashboard import DashboardResponse


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
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

    # Total lessons
    total_lessons = db.query(Lesson).filter(
        Lesson.teacher_id == int(teacher_id)
    ).count()

    # Published lessons
    published_lessons = db.query(Lesson).filter(
        Lesson.teacher_id == int(teacher_id),
        Lesson.status.ilike("published")
    ).count()

    # Draft lessons
    draft_lessons = db.query(Lesson).filter(
        Lesson.teacher_id == int(teacher_id),
        Lesson.status.ilike("draft")
    ).count()

    # Archived lessons
    archived_lessons = db.query(Lesson).filter(
        Lesson.teacher_id == int(teacher_id),
        Lesson.status.ilike("archived")
    ).count()

    # Total classes
    total_classes = db.query(Lesson.class_name).filter(
        Lesson.teacher_id == int(teacher_id)
    ).distinct().count()

    # Total subjects
    total_subjects = db.query(Lesson.subject).filter(
        Lesson.teacher_id == int(teacher_id)
    ).distinct().count()

    # Total topics
    total_topics = db.query(Lesson.topic).filter(
        Lesson.teacher_id == int(teacher_id)
    ).distinct().count()

    # Recent lessons
    recent_lessons = db.query(Lesson).filter(
        Lesson.teacher_id == int(teacher_id)
    ).order_by(
        desc(Lesson.created_at)
    ).limit(5).all()

    recent_lessons_count = len(recent_lessons)

    # Most recently updated lesson
    last_updated_lesson = db.query(Lesson).filter(
        Lesson.teacher_id == int(teacher_id)
    ).order_by(
        desc(Lesson.updated_at)
    ).first()

    last_updated_lesson = (
        last_updated_lesson.updated_at
        if last_updated_lesson
        else None
    )

    return {
        "teacher_id": int(teacher_id),
        "teacher_name": teacher.full_name,
        "teacher_email": teacher.email,
        "total_lessons": total_lessons,
        "published_lessons": published_lessons,
        "draft_lessons": draft_lessons,
        "archived_lessons": archived_lessons,
        "total_subjects": total_subjects,
        "total_classes": total_classes,
        "total_topics": total_topics,
        "recent_lessons_count": recent_lessons_count,
        "last_updated_lesson": last_updated_lesson,
        "recent_lessons": recent_lessons
    }