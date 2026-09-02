from datetime import datetime
from pydantic import BaseModel


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
    total_subjects: int
    total_classes: int
    total_topics: int
    recent_lessons_count: int
    last_updated_lesson: datetime | None
    recent_lessons: list[RecentLessonResponse]
    