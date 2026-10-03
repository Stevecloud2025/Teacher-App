from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.homework import Homework
from app.models.homework_submission import HomeworkSubmission
from app.schemas.homework_submission import (
    HomeworkSubmissionCreate,
    HomeworkSubmissionResponse
)
from app.api.dependencies import get_current_student


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