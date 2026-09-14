from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class QuizOption(Base):
    __tablename__ = "quiz_options"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    option_text = Column(
        String,
        nullable=False
    )

    is_correct = Column(
        Boolean,
        nullable=False,
        default=False
    )

    position = Column(
        Integer,
        nullable=False,
        default=1
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    question = relationship(
        "Question",
        back_populates="options"
    )