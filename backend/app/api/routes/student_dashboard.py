from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.student import Student
from app.models.quiz_attempt import QuizAttempt
from app.models.homework_submission import HomeworkSubmission
from app.models.attendance import Attendance
from app.models.progress_report import ProgressReport
from app.api.dependencies import get_current_student


router = APIRouter(
    prefix="/student-dashboard",
    tags=["Student Dashboard"]
)


@router.get("/")
def get_student_dashboard(
    student_id: str = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    student_id = int(student_id)

    # Get the logged-in student's profile
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Count submitted quiz attempts
    quiz_count = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id,
        QuizAttempt.submitted == True
    ).count()

    # Count graded homework submissions
    graded_homework_count = db.query(
        HomeworkSubmission
    ).filter(
        HomeworkSubmission.student_id == student_id,
        HomeworkSubmission.grade.isnot(None)
    ).count()

    # Count attendance records
    attendance_records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

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

    # Get recent progress reports
    recent_progress_reports = db.query(
        ProgressReport
    ).filter(
        ProgressReport.student_id == student_id
    ).order_by(
        ProgressReport.created_at.desc()
    ).limit(5).all()

    return {
        "student": {
            "id": student.id,
            "full_name": student.full_name,
            "email": student.email,
            "school_name": student.school_name,
            "class_name": student.class_name,
            "created_at": student.created_at
        },
        "quiz_count": quiz_count,
        "graded_homework_count": graded_homework_count,
        "attendance": {
            "total": attendance_total,
            "present": present_count,
            "late": late_count,
            "absent": absent_count,
            "percentage": round(attendance_percentage, 2)
        },
        "recent_progress_reports": recent_progress_reports
    }