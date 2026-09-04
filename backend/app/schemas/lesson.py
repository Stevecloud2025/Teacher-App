from datetime import datetime
from pydantic import BaseModel, Field


class LessonCreate(BaseModel):
    title: str
    subject: str
    class_name: str
    topic: str
    content: str
    status: str = Field(
    default="draft",
    pattern="^(draft|published|archived)$"
)

class LessonResponse(BaseModel):
    id: int
    title: str
    subject: str
    class_name: str
    topic: str
    content: str
    status: str
    teacher_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LessonSummary(BaseModel):
    id: int
    title: str
    subject: str
    class_name: str
    topic: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class LessonListResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    lessons: list[LessonResponse]

