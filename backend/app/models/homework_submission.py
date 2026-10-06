from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from datetime import datetime

from app.database.database import Base


class HomeworkSubmission(Base):
    __tablename__ = "homework_submissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    homework_id = Column(
        Integer,
        ForeignKey("homework.id"),
        nullable=False
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    submitted_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    status = Column(
        String,
        default="submitted",
        nullable=False
    )

    grade = Column(
        Integer,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )