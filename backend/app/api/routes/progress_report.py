from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.progress_report import ProgressReport
from app.models.student import Student
from app.models.quiz_attempt import QuizAttempt
from app.models.homework_submission import HomeworkSubmission
from app.models.attendance import Attendance
from app.schemas.progress_report import (
    ProgressReportCreate,
    ProgressReportUpdate,
    ProgressReportResponse
)
from app.schemas.performance_summary import PerformanceSummaryResponse

from app.api.dependencies import (
    get_current_teacher,
    get_current_student
)


router = APIRouter(
    prefix="/progress-reports",
    tags=["Progress Reports"]
)


def calculate_performance_summary(
    student_id: int,
    db: Session,
    teacher_id: int | None = None
):
    quiz_attempts = db.query(
        QuizAttempt
    ).filter(
        QuizAttempt.student_id == student_id,
        QuizAttempt.submitted == True,
        QuizAttempt.score.isnot(None),
        QuizAttempt.total_questions.isnot(None),
        QuizAttempt.total_questions > 0
    ).all()

    quiz_percentages = [
        (attempt.score / attempt.total_questions) * 100
        for attempt in quiz_attempts
    ]

    quiz_average = (
        sum(quiz_percentages) / len(quiz_percentages)
        if quiz_percentages
        else 0
    )

    homework_submissions = db.query(
        HomeworkSubmission
    ).filter(
        HomeworkSubmission.student_id == student_id,
        HomeworkSubmission.grade.isnot(None)
    ).all()

    homework_grades = [
        submission.grade
        for submission in homework_submissions
    ]

    homework_average = (
        sum(homework_grades) / len(homework_grades)
        if homework_grades
        else 0
    )

    attendance_query = db.query(
        Attendance
    ).filter(
        Attendance.student_id == student_id
    )

    if teacher_id is not None:
        attendance_query = attendance_query.filter(
            Attendance.teacher_id == teacher_id
        )

    attendance_records = attendance_query.all()

    attendance_total = len(attendance_records)

    present_count = sum(
        1 for record in attendance_records
        if record.status.lower() == "present"
    )

    late_count = sum(
        1 for record in attendance_records
        if record.status.lower() == "late"
    )

    absent_count = sum(
        1 for record in attendance_records
        if record.status.lower() == "absent"
    )

    attendance_percentage = (
        (present_count / attendance_total) * 100
        if attendance_total
        else 0
    )

    return PerformanceSummaryResponse(
        student_id=student_id,
        quiz_average=round(quiz_average, 2),
        quiz_count=len(quiz_attempts),
        homework_average=round(homework_average, 2),
        graded_homework_count=len(homework_submissions),
        attendance_percentage=round(attendance_percentage, 2),
        attendance_total=attendance_total,
        present_count=present_count,
        late_count=late_count,
        absent_count=absent_count
    )


@router.get(
    "/my/summary",
    response_model=PerformanceSummaryResponse
)
def get_my_performance_summary(
    student_id: str = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    student_id = int(student_id)

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return calculate_performance_summary(
        student_id=student_id,
        db=db
    )


@router.get(
    "/my",
    response_model=list[ProgressReportResponse]
)
def get_my_progress_reports(
    student_id: str = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    student_id = int(student_id)

    return db.query(
        ProgressReport
    ).filter(
        ProgressReport.student_id == student_id
    ).order_by(
        ProgressReport.created_at.desc()
    ).all()


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
def get_all_progress_reports(
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
    "/student/{student_id}/summary",
    response_model=PerformanceSummaryResponse
)
def get_student_performance_summary(
    student_id: int,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return calculate_performance_summary(
        student_id=student_id,
        db=db,
        teacher_id=teacher_id
    )


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