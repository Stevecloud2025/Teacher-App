from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.quiz import Quiz
from app.models.lesson import Lesson
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    QuizDetailResponse,
    QuizUpdate
)
from app.api.dependencies import get_current_teacher


router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)


@router.post("/", response_model=QuizResponse)
def create_quiz(
    quiz: QuizCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(
        Lesson.id == quiz.lesson_id,
        Lesson.teacher_id == int(teacher_id)
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    new_quiz = Quiz(
        title=quiz.title,
        description=quiz.description,
        lesson_id=quiz.lesson_id,
        teacher_id=int(teacher_id),
        status=quiz.status
    )

    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return new_quiz


@router.get("/", response_model=list[QuizResponse])
def get_quizzes(
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    quizzes = db.query(Quiz).filter(
        Quiz.teacher_id == int(teacher_id)
    ).order_by(
        Quiz.created_at.desc()
    ).all()

    return quizzes

@router.get("/{quiz_id}", response_model=QuizDetailResponse)
def get_quiz(
    quiz_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id,
        Quiz.teacher_id == int(teacher_id)
    ).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    return quiz

    @router.put("/{quiz_id}", response_model=QuizResponse)
    def update_quiz(
    quiz_id: int,
    quiz: QuizUpdate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
     existing_quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id,
        Quiz.teacher_id == int(teacher_id)
    ).first()

    if not existing_quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    existing_quiz.title = quiz.title
    existing_quiz.description = quiz.description
    existing_quiz.status = quiz.status

    db.commit()
    db.refresh(existing_quiz)

    return existing_quiz

    @router.delete("/{quiz_id}")
    def delete_quiz(
    quiz_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
     quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id,
        Quiz.teacher_id == int(teacher_id)
    ).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    db.delete(quiz)
    db.commit()

    return {
        "message": "Quiz deleted successfully"
    }