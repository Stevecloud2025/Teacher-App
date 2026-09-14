from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.option import QuizOption
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    QuestionValidationResponse,
    QuestionReorder
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

    last_question = db.query(Question).filter(
        Question.quiz_id == question.quiz_id
    ).order_by(
        Question.position.desc()
    ).first()

    next_position = (
        last_question.position + 1
        if last_question
        else 1
    )

    new_question = Question(
        question_text=question.question_text,
        question_type=question.question_type,
        quiz_id=question.quiz_id,
        correct_answer=question.correct_answer,
        position=next_position
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


@router.get(
    "/quiz/{quiz_id}",
    response_model=list[QuestionResponse]
)
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
    ).order_by(
        Question.position.asc()
    ).all()

    return questions


@router.get(
    "/{question_id}/validate",
    response_model=QuestionValidationResponse
)
def validate_question(
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

    has_options = len(options) > 0

    correct_option_count = sum(
        option.is_correct for option in options
    )

    has_correct_option = correct_option_count > 0

    if question.question_type == "multiple_choice":
        is_valid = (
            has_options
            and correct_option_count == 1
        )
    elif question.question_type == "true_false":
        is_valid = question.correct_answer.lower() in [
            "true",
            "false"
        ]
    else:
        is_valid = bool(
            question.correct_answer.strip()
        )

    return {
        "question_id": question.id,
        "question_type": question.question_type,
        "has_options": has_options,
        "has_correct_option": has_correct_option,
        "is_valid": is_valid
    }


@router.get(
    "/{question_id}",
    response_model=QuestionResponse
)
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


@router.put(
    "/{question_id}",
    response_model=QuestionResponse
)
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
    existing_question.position = question.position

    db.commit()
    db.refresh(existing_question)

    return existing_question


@router.delete(
    "/{question_id}"
)
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

@router.patch(
    "/{question_id}/reorder",
    response_model=QuestionResponse
)
def reorder_question(
    question_id: int,
    reorder: QuestionReorder,
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

    quiz_questions = db.query(Question).filter(
        Question.quiz_id == question.quiz_id
    ).order_by(
        Question.position.asc()
    ).all()

    if reorder.position > len(quiz_questions):
        raise HTTPException(
            status_code=400,
            detail="Position is outside the range of questions in this quiz"
        )

    old_position = question.position
    new_position = reorder.position

    if old_position == new_position:
        return question

    if new_position < old_position:
        for item in quiz_questions:
            if (
                item.id != question.id
                and new_position <= item.position < old_position
            ):
                item.position += 1

    else:
        for item in quiz_questions:
            if (
                item.id != question.id
                and old_position < item.position <= new_position
            ):
                item.position -= 1

    question.position = new_position

    db.commit()
    db.refresh(question)

    return question