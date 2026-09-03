from datetime import datetime
from pydantic import BaseModel
from app.schemas.lesson import LessonSummary


class RecentLessonResponse(BaseModel):
    id: int
    title: str
    subject: str
    class_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    teacher_id: int
    teacher_name: str
    teacher_email: str

    total_lessons: int
    published_lessons: int
    draft_lessons: int
    archived_lessons: int

    total_subjects: int
    total_classes: int
    total_topics: int

    recent_lessons_count: int
    last_updated_lesson: datetime | None
    recent_lessons: list[LessonSummary]
    