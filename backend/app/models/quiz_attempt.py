from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        nullable=False
    )

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )

    score = Column(
        Integer,
        nullable=True
    )

    total_questions = Column(
        Integer,
        nullable=True
    )

    submitted = Column(
        Boolean,
        nullable=False,
        default=False
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    submitted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    quiz = relationship(
        "Quiz",
        back_populates="attempts"
    )

    answers = relationship(
        "QuizAttemptAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan"
    )