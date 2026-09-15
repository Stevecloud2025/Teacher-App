from pydantic import BaseModel


class QuizAttemptAnswerCreate(BaseModel):
    question_id: int
    selected_option_id: int | None = None
    answer_text: str | None = None


class QuizAttemptAnswerResponse(BaseModel):
    id: int
    attempt_id: int
    question_id: int
    selected_option_id: int | None
    answer_text: str | None
    is_correct: bool | None

    class Config:
        from_attributes = True