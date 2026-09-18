from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.quiz_attempt_answer import QuizAttemptAnswer
from app.models.question import Question
from app.models.option import QuizOption

from app.schemas.attempt import (
    QuizAttemptCreate,
    QuizAttemptResponse,
    QuizAttemptResultResponse
)

from app.schemas.attempt_answer import (
    QuizAttemptAnswerCreate,
    QuizAttemptAnswerResponse
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
    existing_attempt = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == attempt.student_id,
        QuizAttempt.quiz_id == attempt.quiz_id
    ).first()

    if existing_attempt:
        raise HTTPException(
            status_code=400,
            detail="This student has already attempted this quiz"
        )

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


@router.post(
    "/{attempt_id}/answers",
    response_model=QuizAttemptAnswerResponse
)
def submit_quiz_answer(
    attempt_id: int,
    answer: QuizAttemptAnswerCreate,
    db: Session = Depends(get_db)
):
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id,
        QuizAttempt.submitted == False
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Active quiz attempt not found"
        )

    question = db.query(Question).filter(
        Question.id == answer.question_id,
        Question.quiz_id == attempt.quiz_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found in this quiz"
        )

    existing_answer = db.query(QuizAttemptAnswer).filter(
        QuizAttemptAnswer.attempt_id == attempt_id,
        QuizAttemptAnswer.question_id == answer.question_id
    ).first()

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="This question has already been answered"
        )

    is_correct = False

    if question.question_type == "multiple_choice":
        if answer.selected_option_id is None:
            raise HTTPException(
                status_code=400,
                detail="A multiple-choice question requires an option"
            )

        selected_option = db.query(QuizOption).filter(
            QuizOption.id == answer.selected_option_id,
            QuizOption.question_id == question.id
        ).first()

        if not selected_option:
            raise HTTPException(
                status_code=400,
                detail="Selected option does not belong to this question"
            )

        is_correct = selected_option.is_correct

    elif question.question_type == "true_false":
        if not answer.answer_text:
            raise HTTPException(
                status_code=400,
                detail="A true/false question requires an answer"
            )

        is_correct = (
            answer.answer_text.strip().lower()
            == question.correct_answer.strip().lower()
        )

    elif question.question_type == "short_answer":
        if not answer.answer_text:
            raise HTTPException(
                status_code=400,
                detail="A short-answer question requires an answer"
            )

        is_correct = (
            answer.answer_text.strip().lower()
            == question.correct_answer.strip().lower()
        )

    new_answer = QuizAttemptAnswer(
        attempt_id=attempt_id,
        question_id=answer.question_id,
        selected_option_id=answer.selected_option_id,
        answer_text=answer.answer_text,
        is_correct=is_correct
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer


@router.get(
    "/{attempt_id}/answers",
    response_model=list[QuizAttemptAnswerResponse]
)
def get_attempt_answers(
    attempt_id: int,
    db: Session = Depends(get_db)
):
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Quiz attempt not found"
        )

    answers = db.query(QuizAttemptAnswer).filter(
        QuizAttemptAnswer.attempt_id == attempt_id
    ).order_by(
        QuizAttemptAnswer.question_id.asc()
    ).all()

    return answers


@router.post(
    "/{attempt_id}/submit",
    response_model=QuizAttemptResponse
)
def submit_quiz_attempt(
    attempt_id: int,
    db: Session = Depends(get_db)
):
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Quiz attempt not found"
        )

    if attempt.submitted:
        raise HTTPException(
            status_code=400,
            detail="Quiz attempt has already been submitted"
        )

    questions = db.query(Question).filter(
        Question.quiz_id == attempt.quiz_id
    ).all()

    answers = db.query(QuizAttemptAnswer).filter(
        QuizAttemptAnswer.attempt_id == attempt_id
    ).all()

    total_questions = len(questions)

    score = sum(
        1
        for answer in answers
        if answer.is_correct
    )

    attempt.score = score
    attempt.total_questions = total_questions
    attempt.submitted = True
    attempt.submitted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(attempt)

    return attempt


@router.get(
    "/{attempt_id}/result",
    response_model=QuizAttemptResultResponse
)
def get_quiz_attempt_result(
    attempt_id: int,
    db: Session = Depends(get_db)
):
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Quiz attempt not found"
        )

    if not attempt.submitted:
        raise HTTPException(
            status_code=400,
            detail="Quiz attempt has not been submitted"
        )

    score = attempt.score or 0
    total_questions = attempt.total_questions or 0

    percentage = (
        (score / total_questions) * 100
        if total_questions > 0
        else 0
    )

    return {
        "attempt_id": attempt.id,
        "student_id": attempt.student_id,
        "quiz_id": attempt.quiz_id,
        "score": score,
        "total_questions": total_questions,
        "percentage": round(percentage, 2),
        "submitted": attempt.submitted,
        "submitted_at": attempt.submitted_at
    }