from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.homework import Homework
from app.models.homework_submission import HomeworkSubmission
from app.schemas.homework_submission import (
    HomeworkSubmissionCreate,
    HomeworkSubmissionGrade,
    HomeworkSubmissionResponse
)
from app.api.dependencies import (
    get_current_student,
    get_current_teacher
)


router = APIRouter(
    prefix="/homework-submissions",
    tags=["Homework Submissions"]
)


@router.post(
    "/",
    response_model=HomeworkSubmissionResponse
)
def submit_homework(
    submission: HomeworkSubmissionCreate,
    student_id: str = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    student_id = int(student_id)

    homework = db.query(Homework).filter(
        Homework.id == submission.homework_id
    ).first()

    if not homework:
        raise HTTPException(
            status_code=404,
            detail="Homework not found"
        )

    existing_submission = db.query(
        HomeworkSubmission
    ).filter(
        HomeworkSubmission.homework_id == submission.homework_id,
        HomeworkSubmission.student_id == student_id
    ).first()

    if existing_submission:
        raise HTTPException(
            status_code=400,
            detail="You have already submitted this homework"
        )

    new_submission = HomeworkSubmission(
        homework_id=submission.homework_id,
        student_id=student_id,
        content=submission.content
    )

    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission


@router.get(
    "/",
    response_model=list[HomeworkSubmissionResponse]
)
def get_my_submissions(
    student_id: str = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    student_id = int(student_id)

    return db.query(
        HomeworkSubmission
    ).filter(
        HomeworkSubmission.student_id == student_id
    ).order_by(
        HomeworkSubmission.submitted_at.desc()
    ).all()


@router.get(
    "/teacher",
    response_model=list[HomeworkSubmissionResponse]
)
def get_homework_submissions_for_teacher(
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    return db.query(
        HomeworkSubmission
    ).join(
        Homework,
        Homework.id == HomeworkSubmission.homework_id
    ).filter(
        Homework.teacher_id == teacher_id
    ).order_by(
        HomeworkSubmission.submitted_at.desc()
    ).all()


@router.put(
    "/{submission_id}/grade",
    response_model=HomeworkSubmissionResponse
)
def grade_homework_submission(
    submission_id: int,
    grading: HomeworkSubmissionGrade,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    submission = db.query(
        HomeworkSubmission
    ).join(
        Homework,
        Homework.id == HomeworkSubmission.homework_id
    ).filter(
        HomeworkSubmission.id == submission_id,
        Homework.teacher_id == teacher_id
    ).first()

    if not submission:
        raise HTTPException(
            status_code=404,
            detail="Homework submission not found"
        )

    submission.grade = grading.grade
    submission.feedback = grading.feedback
    submission.status = "graded"

    db.commit()
    db.refresh(submission)

    return submission