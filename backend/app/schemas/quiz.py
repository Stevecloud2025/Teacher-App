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


class QuizOptionResponseNested(BaseModel):
    id: int
    option_text: str
    is_correct: bool

    class Config:
        from_attributes = True


class QuestionResponseNested(BaseModel):
    id: int
    question_text: str
    question_type: str
    correct_answer: str
    position: int
    options: list[QuizOptionResponseNested] = []

    class Config:
        from_attributes = True


class QuizDetailResponse(BaseModel):
    id: int
    title: str
    description: str | None
    lesson_id: int
    teacher_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    questions: list[QuestionResponseNested] = []

    class Config:
        from_attributes = True


class QuizUpdate(BaseModel):
    title: str
    description: str | None = None
    status: str = Field(
        default="draft",
        pattern="^(draft|published|archived)$"
    )


class QuizStatusUpdate(BaseModel):
    status: str = Field(
        pattern="^(draft|published|archived)$"
    )


class QuizValidationResponse(BaseModel):
    quiz_id: int
    total_questions: int
    valid_questions: int
    invalid_questions: int
    is_valid: bool