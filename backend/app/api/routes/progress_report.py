from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.progress_report import ProgressReport
from app.models.student import Student
from app.schemas.progress_report import (
    ProgressReportCreate,
    ProgressReportUpdate,
    ProgressReportResponse
)
from app.api.dependencies import get_current_teacher


router = APIRouter(
    prefix="/progress-reports",
    tags=["Progress Reports"]
)


@router.post(
    "/",
    response_model=ProgressReportResponse
)
def create_progress_report(
    report: ProgressReportCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    student = db.query(Student).filter(
        Student.id == report.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_report = ProgressReport(
        student_id=report.student_id,
        teacher_id=teacher_id,
        term=report.term,
        session=report.session,
        overall_grade=report.overall_grade,
        teacher_comment=report.teacher_comment
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report


@router.get(
    "/",
    response_model=list[ProgressReportResponse]
)
def get_my_progress_reports(
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    return db.query(
        ProgressReport
    ).filter(
        ProgressReport.teacher_id == teacher_id
    ).order_by(
        ProgressReport.created_at.desc()
    ).all()


@router.get(
    "/student/{student_id}",
    response_model=list[ProgressReportResponse]
)
def get_student_progress_reports(
    student_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    return db.query(
        ProgressReport
    ).filter(
        ProgressReport.student_id == student_id,
        ProgressReport.teacher_id == teacher_id
    ).order_by(
        ProgressReport.created_at.desc()
    ).all()


@router.get(
    "/{report_id}",
    response_model=ProgressReportResponse
)
def get_progress_report(
    report_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    report = db.query(
        ProgressReport
    ).filter(
        ProgressReport.id == report_id,
        ProgressReport.teacher_id == teacher_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Progress report not found"
        )

    return report


@router.put(
    "/{report_id}",
    response_model=ProgressReportResponse
)
def update_progress_report(
    report_id: int,
    report_data: ProgressReportUpdate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    report = db.query(
        ProgressReport
    ).filter(
        ProgressReport.id == report_id,
        ProgressReport.teacher_id == teacher_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Progress report not found"
        )

    if report_data.term is not None:
        report.term = report_data.term

    if report_data.session is not None:
        report.session = report_data.session

    if report_data.overall_grade is not None:
        report.overall_grade = report_data.overall_grade

    if report_data.teacher_comment is not None:
        report.teacher_comment = report_data.teacher_comment

    db.commit()
    db.refresh(report)

    return report


@router.delete(
    "/{report_id}"
)
def delete_progress_report(
    report_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    report = db.query(
        ProgressReport
    ).filter(
        ProgressReport.id == report_id,
        ProgressReport.teacher_id == teacher_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Progress report not found"
        )

    db.delete(report)
    db.commit()

    return {
        "message": "Progress report deleted successfully"
    }