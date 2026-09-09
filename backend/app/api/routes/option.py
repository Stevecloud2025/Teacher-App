from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.option import QuizOption
from app.models.question import Question
from app.models.quiz import Quiz
from app.schemas.option import QuizOptionCreate, QuizOptionResponse
from app.api.dependencies import get_current_teacher


router = APIRouter(
    prefix="/options",
    tags=["Quiz Options"]
)


@router.post("/", response_model=QuizOptionResponse)
def create_option(
    option: QuizOptionCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    question = db.query(Question).join(
        Question.quiz
    ).filter(
        Question.id == option.question_id,
        Quiz.teacher_id == int(teacher_id)
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    new_option = QuizOption(
        option_text=option.option_text,
        is_correct=option.is_correct,
        question_id=option.question_id
    )

    db.add(new_option)
    db.commit()
    db.refresh(new_option)

    return new_option