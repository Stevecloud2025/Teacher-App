from datetime import datetime
from pydantic import BaseModel, Field


class QuizCreate(BaseModel):
    title: str
    description: str | None = None
    lesson_id: int
    status: str = Field(
        default="draft",
        pattern="^(draft|published|archived)$"
    )


class QuizResponse(BaseModel):
    id: int
    title: str
    description: str | None
    lesson_id: int
    teacher_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True