from datetime import datetime
from pydantic import BaseModel


class HomeworkSubmissionCreate(BaseModel):
    homework_id: int
    content: str


class HomeworkSubmissionResponse(BaseModel):
    id: int
    homework_id: int
    student_id: int
    content: str
    submitted_at: datetime
    status: str

    class Config:
        from_attributes = True