from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question_text = Column(
        Text,
        nullable=False
    )

    question_type = Column(
        String,
        nullable=False,
        default="multiple_choice"
    )

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )

    correct_answer = Column(
        String,
        nullable=False
    )

    quiz = relationship(
        "Quiz",
        back_populates="questions"
    )
    options = relationship(
    "QuizOption",
    back_populates="question",
    cascade="all, delete-orphan"
)