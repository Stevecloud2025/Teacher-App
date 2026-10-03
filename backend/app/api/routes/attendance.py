from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.attendance import Attendance
from app.models.student import Student
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.api.dependencies import get_current_teacher


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/", response_model=AttendanceResponse)
def mark_attendance(
    attendance: AttendanceCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    # Check that the student exists
    student = db.query(Student).filter(
        Student.id == attendance.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check if attendance has already been marked
    existing_attendance = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.teacher_id == teacher_id,
        Attendance.date == attendance.date
    ).first()

    if existing_attendance:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this student on this date"
        )

    new_attendance = Attendance(
        student_id=attendance.student_id,
        teacher_id=teacher_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


@router.get("/", response_model=list[AttendanceResponse])
def get_attendance(
    attendance_date: date | None = None,
    student_id: int | None = None,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    query = db.query(Attendance).filter(
        Attendance.teacher_id == teacher_id
    )

    if attendance_date:
        query = query.filter(
            Attendance.date == attendance_date
        )

    if student_id:
        query = query.filter(
            Attendance.student_id == student_id
        )

    return query.order_by(
        Attendance.date.desc()
    ).all()


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceCreate,
    teacher_id: str = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    teacher_id = int(teacher_id)

    existing_attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id,
        Attendance.teacher_id == teacher_id
    ).first()

    if not existing_attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    # Check whether the new student/date combination
    # already has another attendance record
    duplicate = db.query(Attendance).filter(
        Attendance.id != attendance_id,
        Attendance.student_id == attendance.student_id,
        Attendance.teacher_id == teacher_id,
        Attendance.date == attendance.date
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this student on this date"
        )

    existing_attendance.student_id = attendance.student_id
    existing_attendance.date = attendance.date
    existing_attendance.status = attendance.status

    db.commit()
    db.refresh(existing_attendance)

    return existing_attendance