from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.option import QuizOption
from app.models.question import Question
from app.models.quiz import Quiz
from app.schemas.option import (
    QuizOptionCreate,
    QuizOptionResponse,
    QuizOptionUpdate
)
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

    if option.is_correct:
        existing_correct_option = db.query(QuizOption).filter(
        QuizOption.question_id == option.question_id,
        QuizOption.is_correct == True
    ).first()

    if existing_correct_option:
        raise HTTPException(
            status_code=400,
            detail="This question already has a correct option"
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

@router.get("/question/{question_id}", response_model=list[QuizOptionResponse])
def get_question_options(
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

    options = db.query(QuizOption).filter(
        QuizOption.question_id == question_id
    ).all()

    return options

@router.get("/{option_id}", response_model=QuizOptionResponse)
def get_option(
    option_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    option = db.query(QuizOption).join(
        QuizOption.question
    ).join(
        Question.quiz
    ).filter(
        QuizOption.id == option_id,
        QuizOption.question.has(
            Question.quiz.has(
                Quiz.teacher_id == int(teacher_id)
            )
        )
    ).first()

    if not option:
        raise HTTPException(
            status_code=404,
            detail="Option not found"
        )

    return option

    @router.put("/{option_id}", response_model=QuizOptionResponse)
    def update_option(
    option_id: int,
    option: QuizOptionUpdate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
     existing_option = db.query(QuizOption).join(
        QuizOption.question
    ).join(
        Question.quiz
    ).filter(
        QuizOption.id == option_id,
        QuizOption.question.has(
            Question.quiz.has(
                Quiz.teacher_id == int(teacher_id)
            )
        )
    ).first()

    if not existing_option:
        raise HTTPException(
            status_code=404,
            detail="Option not found"
        )

    if option.is_correct:
        existing_correct_option = db.query(QuizOption).filter(
        QuizOption.question_id == existing_option.question_id,
        QuizOption.is_correct == True,
        QuizOption.id != existing_option.id
    ).first()

    if existing_correct_option:
        raise HTTPException(
            status_code=400,
            detail="This question already has a different correct option"
        )

    existing_option.option_text = option.option_text
    existing_option.is_correct = option.is_correct

    db.commit()
    db.refresh(existing_option)

    return existing_option

@router.delete("/{option_id}")
def delete_option(
    option_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    option = db.query(QuizOption).join(
        QuizOption.question
    ).join(
        Question.quiz
    ).filter(
        QuizOption.id == option_id,
        QuizOption.question.has(
            Question.quiz.has(
                Quiz.teacher_id == int(teacher_id)
            )
        )
    ).first()

    if not option:
        raise HTTPException(
            status_code=404,
            detail="Option not found"
        )

    db.delete(option)
    db.commit()

    return {
        "message": "Option deleted successfully"
    }