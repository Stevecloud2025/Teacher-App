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
    position: int

    class Config:
        from_attributes = True


class QuestionUpdate(BaseModel):
    question_text: str
    question_type: str = Field(
        default="multiple_choice",
        pattern="^(multiple_choice|true_false|short_answer)$"
    )
    correct_answer: str
    position: int = Field(default=1, ge=1)


class QuestionValidationResponse(BaseModel):
    question_id: int
    question_type: str
    has_options: bool
    has_correct_option: bool
    is_valid: bool