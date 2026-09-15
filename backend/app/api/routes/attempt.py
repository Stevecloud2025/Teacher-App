from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.schemas.attempt import (
    QuizAttemptCreate,
    QuizAttemptResponse
)


router = APIRouter(
    prefix="/attempts",
    tags=["Quiz Attempts"]
)


@router.post(
    "/",
    response_model=QuizAttemptResponse
)
def start_quiz_attempt(
    attempt: QuizAttemptCreate,
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(
        Quiz.id == attempt.quiz_id,
        Quiz.status == "published"
    ).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Published quiz not found"
        )

    new_attempt = QuizAttempt(
        student_id=attempt.student_id,
        quiz_id=attempt.quiz_id,
        submitted=False
    )

    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)

    return new_attempt