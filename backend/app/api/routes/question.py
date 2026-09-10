from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.question import Question
from app.models.quiz import Quiz
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate
)
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


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    question = db.query(Question).join(
        Question.quiz
    ).filter(
        Question.id == question_id,
        Quiz.teacher_id == int(teacher_id)
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question

    @router.put("/{question_id}", response_model=QuestionResponse)
    def update_question(
    question_id: int,
    question: QuestionUpdate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
     existing_question = db.query(Question).join(
        Question.quiz
    ).filter(
        Question.id == question_id,
        Quiz.teacher_id == int(teacher_id)
    ).first()

    if not existing_question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    existing_question.question_text = question.question_text
    existing_question.question_type = question.question_type
    existing_question.correct_answer = question.correct_answer

    db.commit()
    db.refresh(existing_question)

    return existing_question

@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    question = db.query(Question).join(
        Question.quiz
    ).filter(
        Question.id == question_id,
        Quiz.teacher_id == int(teacher_id)
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    db.delete(question)
    db.commit()

    return {
        "message": "Question deleted successfully"
    }

@router.get("/quiz/{quiz_id}", response_model=list[QuestionResponse])
def get_quiz_questions(
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

    questions = db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()

    return questions