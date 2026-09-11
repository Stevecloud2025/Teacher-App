from pydantic import BaseModel


class QuizOptionCreate(BaseModel):
    option_text: str
    is_correct: bool = False
    question_id: int


class QuizOptionResponse(BaseModel):
    id: int
    option_text: str
    is_correct: bool
    question_id: int

    class Config:
        from_attributes = True


class QuizOptionUpdate(BaseModel):
    option_text: str
    is_correct: bool = False