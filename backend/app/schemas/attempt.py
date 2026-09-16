from datetime import datetime

from pydantic import BaseModel


class QuizAttemptCreate(BaseModel):
    quiz_id: int
    student_id: int


class QuizAttemptResponse(BaseModel):
    id: int
    student_id: int
    quiz_id: int
    score: int | None
    total_questions: int | None
    submitted: bool
    started_at: datetime
    submitted_at: datetime | None

    class Config:
        from_attributes = True