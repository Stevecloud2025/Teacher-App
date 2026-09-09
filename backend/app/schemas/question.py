from pydantic import BaseModel, Field


class QuestionCreate(BaseModel):
    question_text: str
    question_type: str = Field(
        default="multiple_choice",
        pattern="^(multiple_choice|true_false|short_answer)$"
    )
    quiz_id: int
    correct_answer: str


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    quiz_id: int
    correct_answer: str

    class Config:
        from_attributes = True