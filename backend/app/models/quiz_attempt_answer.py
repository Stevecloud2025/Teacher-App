from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class QuizAttemptAnswer(Base):
    __tablename__ = "quiz_attempt_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    attempt_id = Column(
        Integer,
        ForeignKey("quiz_attempts.id"),
        nullable=False
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    selected_option_id = Column(
        Integer,
        ForeignKey("quiz_options.id"),
        nullable=True
    )

    answer_text = Column(
        String,
        nullable=True
    )

    is_correct = Column(
        Boolean,
        nullable=True
    )

    attempt = relationship(
        "QuizAttempt",
        back_populates="answers"
    )

    question = relationship(
        "Question"
    )

    selected_option = relationship(
        "QuizOption"
    )