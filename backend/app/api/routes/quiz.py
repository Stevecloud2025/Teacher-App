from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.quiz import Quiz
from app.models.lesson import Lesson
from app.models.question import Question
from app.models.option import QuizOption
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    QuizDetailResponse,
    QuizUpdate,
    StudentQuizResponse,
    QuizValidationResponse,
    QuizStatusUpdate,
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
        status=quiz.status,
        time_limit=quiz.time_limit
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


@router.get(
    "/quiz/{quiz_id}/validate",
    response_model=QuizValidationResponse
)
def validate_quiz(
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

    total_questions = len(questions)
    valid_questions = 0
    question_results = []

    for question in questions:
        options = db.query(QuizOption).filter(
            QuizOption.question_id == question.id
        ).all()

        has_options = len(options) > 0

        correct_option_count = sum(
            option.is_correct for option in options
        )

        if question.question_type == "multiple_choice":
            is_valid = (
                has_options
                and correct_option_count == 1
            )

            if not has_options:
                reason = "Question has no options"
            elif correct_option_count == 0:
                reason = "Question has no correct option"
            elif correct_option_count > 1:
                reason = "Question has more than one correct option"
            else:
                reason = "Question is valid"

        elif question.question_type == "true_false":
            is_valid = question.correct_answer.lower() in [
                "true",
                "false"
            ]

            if is_valid:
                reason = "Question is valid"
            else:
                reason = (
                    "True/false question must have "
                    "a valid correct answer"
                )

        else:
            is_valid = bool(
                question.correct_answer.strip()
            )

            if is_valid:
                reason = "Question is valid"
            else:
                reason = "Question must have a correct answer"

        if is_valid:
            valid_questions += 1

        question_results.append(
            {
                "question_id": question.id,
                "question_type": question.question_type,
                "is_valid": is_valid,
                "reason": reason
            }
        )

    invalid_questions = total_questions - valid_questions

    is_valid = (
        total_questions > 0
        and invalid_questions == 0
    )

    return {
        "quiz_id": quiz.id,
        "total_questions": total_questions,
        "valid_questions": valid_questions,
        "invalid_questions": invalid_questions,
        "is_valid": is_valid,
        "questions": question_results
    }


@router.get(
    "/student/{quiz_id}",
    response_model=StudentQuizResponse
)
def get_student_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id,
        Quiz.status == "published"
    ).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Published quiz not found"
        )

    return quiz


@router.get(
    "/{quiz_id}",
    response_model=QuizDetailResponse
)
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


@router.post(
    "/{quiz_id}/duplicate",
    response_model=QuizResponse
)
def duplicate_quiz(
    quiz_id: int,
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

    new_quiz = Quiz(
        title=f"{existing_quiz.title} (Copy)",
        description=existing_quiz.description,
        lesson_id=existing_quiz.lesson_id,
        teacher_id=int(teacher_id),
        status="draft",
        time_limit=existing_quiz.time_limit
    )

    db.add(new_quiz)
    db.flush()

    questions = db.query(Question).filter(
        Question.quiz_id == existing_quiz.id
    ).order_by(
        Question.position.asc()
    ).all()

    for question in questions:
        new_question = Question(
            question_text=question.question_text,
            question_type=question.question_type,
            quiz_id=new_quiz.id,
            correct_answer=question.correct_answer,
            position=question.position
        )

        db.add(new_question)
        db.flush()

        options = db.query(QuizOption).filter(
            QuizOption.question_id == question.id
        ).order_by(
            QuizOption.position.asc()
        ).all()

        for option in options:
            new_option = QuizOption(
                option_text=option.option_text,
                is_correct=option.is_correct,
                position=option.position,
                question_id=new_question.id
            )

            db.add(new_option)

    db.commit()
    db.refresh(new_quiz)

    return new_quiz


@router.put(
    "/{quiz_id}",
    response_model=QuizResponse
)
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

    if quiz.status == "published":
        questions = db.query(Question).filter(
            Question.quiz_id == quiz_id
        ).all()

        if not questions:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Quiz must have at least one question "
                    "before publishing"
                )
            )

        for question in questions:
            options = db.query(QuizOption).filter(
                QuizOption.question_id == question.id
            ).all()

            if question.question_type == "multiple_choice":
                has_options = len(options) > 0

                correct_option_count = sum(
                    option.is_correct for option in options
                )

                if not has_options or correct_option_count != 1:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "All multiple-choice questions must "
                            "have options and exactly one correct "
                            "answer before publishing"
                        )
                    )

            elif question.question_type == "true_false":
                if question.correct_answer.lower() not in [
                    "true",
                    "false"
                ]:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "True/false questions must have "
                            "a valid correct answer before publishing"
                        )
                    )

            elif question.question_type == "short_answer":
                if not question.correct_answer.strip():
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "Short-answer questions must have "
                            "a correct answer before publishing"
                        )
                    )

    existing_quiz.title = quiz.title
    existing_quiz.description = quiz.description
    existing_quiz.status = quiz.status
    existing_quiz.time_limit = quiz.time_limit

    db.commit()
    db.refresh(existing_quiz)

    return existing_quiz


@router.delete(
    "/{quiz_id}"
)
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


@router.patch(
    "/{quiz_id}/status",
    response_model=QuizResponse
)
def update_quiz_status(
    quiz_id: int,
    quiz_status: QuizStatusUpdate,
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

    if quiz_status.status == "published":
        questions = db.query(Question).filter(
            Question.quiz_id == quiz_id
        ).all()

        if not questions:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Quiz must have at least one question "
                    "before publishing"
                )
            )

        for question in questions:
            options = db.query(QuizOption).filter(
                QuizOption.question_id == question.id
            ).all()

            if question.question_type == "multiple_choice":
                has_options = len(options) > 0

                correct_option_count = sum(
                    option.is_correct for option in options
                )

                if not has_options or correct_option_count != 1:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "All multiple-choice questions must "
                            "have options and exactly one correct "
                            "answer before publishing"
                        )
                    )

            elif question.question_type == "true_false":
                if question.correct_answer.lower() not in [
                    "true",
                    "false"
                ]:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "True/false questions must have "
                            "a valid correct answer before publishing"
                        )
                    )

            elif question.question_type == "short_answer":
                if not question.correct_answer.strip():
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "Short-answer questions must have "
                            "a correct answer before publishing"
                        )
                    )

    quiz.status = quiz_status.status

    db.commit()
    db.refresh(quiz)

    return quiz