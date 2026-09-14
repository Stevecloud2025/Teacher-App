from pydantic import BaseModel, Field


class QuizOptionCreate(BaseModel):
    option_text: str
    is_correct: bool = False
    question_id: int


class QuizOptionResponse(BaseModel):
    id: int
    option_text: str
    is_correct: bool
    position: int
    question_id: int

    class Config:
        from_attributes = True


class QuizOptionUpdate(BaseModel):
    option_text: str
    is_correct: bool = False


class QuizOptionReorder(BaseModel):
    position: int = Field(
        ge=1
    )