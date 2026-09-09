from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.question import Question
from app.models.quiz import Quiz
from app.schemas.question import QuestionCreate, QuestionResponse
from app.api.dependencies import get_current_teacher


router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


@router.post("/", response_model=QuestionResponse)
def create_question(
    question: QuestionCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(
        Quiz.id == question.quiz_id,
        Quiz.teacher_id == int(teacher_id)
    ).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    new_question = Question(
        question_text=question.question_text,
        question_type=question.question_type,
        quiz_id=question.quiz_id,
        correct_answer=question.correct_answer
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question