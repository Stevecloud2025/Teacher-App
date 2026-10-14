from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database.database import get_db
from app.models.student import Student
from app.models.progress_report import ProgressReport
from app.models.homework import Homework
from app.models.homework_submission import HomeworkSubmission
from app.api.dependencies import get_current_student
from app.api.routes.progress_report import calculate_performance_summary

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

           # Calculate the student's academic performance
    performance_summary = calculate_performance_summary(
        student_id=student_id,
        db=db
    )

    # Get homework assigned to the student's class
    assigned_homework = db.query(
        Homework
    ).filter(
        Homework.class_name == student.class_name
    ).all()

    total_homework = len(assigned_homework)

    # Get homework submissions made by the student
    submitted_homework_ids = db.query(
        HomeworkSubmission.homework_id
    ).filter(
        HomeworkSubmission.student_id == student_id
    ).distinct().all()

    submitted_homework_ids = {
        item[0] for item in submitted_homework_ids
    }

    # Count submitted assignments that belong to the student's class
    submitted_homework = sum(
        1 for homework in assigned_homework
        if homework.id in submitted_homework_ids
    )

    # Calculate pending homework
    pending_homework = total_homework - submitted_homework

        # Get today's date
    today = date.today()

    # Identify upcoming homework that has not been submitted
    upcoming_homework = [
        {
            "id": homework.id,
            "title": homework.title,
            "subject": homework.subject,
            "due_date": homework.due_date
        }
        for homework in assigned_homework
        if homework.id not in submitted_homework_ids
        and homework.due_date >= today
    ]

    # Identify overdue homework that has not been submitted
    overdue_homework = [
        {
            "id": homework.id,
            "title": homework.title,
            "subject": homework.subject,
            "due_date": homework.due_date
        }
        for homework in assigned_homework
        if homework.id not in submitted_homework_ids
        and homework.due_date < today
    ]
    
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
        "quiz_count": performance_summary.quiz_count,
        "quiz_average": performance_summary.quiz_average,
        "graded_homework_count": performance_summary.graded_homework_count,
        "homework_average": performance_summary.homework_average,
        "homework_overview": {
            "total": total_homework,
            "submitted": submitted_homework,
            "pending": pending_homework
        },
        "upcoming_homework": upcoming_homework,
        "overdue_homework": overdue_homework,
        "attendance": {
            "total": performance_summary.attendance_total,
            "present": performance_summary.present_count,
            "late": performance_summary.late_count,
            "absent": performance_summary.absent_count,
            "percentage": performance_summary.attendance_percentage
        },
        "recent_progress_reports": recent_progress_reports
    }