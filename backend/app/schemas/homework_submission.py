from datetime import datetime
from pydantic import BaseModel


class HomeworkSubmissionCreate(BaseModel):
    homework_id: int
    content: str


class HomeworkSubmissionGrade(BaseModel):
    grade: int
    feedback: str | None = None


class HomeworkSubmissionResponse(BaseModel):
    id: int
    homework_id: int
    student_id: int
    content: str
    submitted_at: datetime
    status: str
    grade: int | None = None
    feedback: str | None = None

    class Config:
        from_attributes = True