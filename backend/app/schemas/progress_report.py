from datetime import datetime
from pydantic import BaseModel


class ProgressReportCreate(BaseModel):
    student_id: int
    term: str
    session: str
    overall_grade: str | None = None
    teacher_comment: str | None = None


class ProgressReportUpdate(BaseModel):
    term: str | None = None
    session: str | None = None
    overall_grade: str | None = None
    teacher_comment: str | None = None


class ProgressReportResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    term: str
    session: str
    overall_grade: str | None = None
    teacher_comment: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True