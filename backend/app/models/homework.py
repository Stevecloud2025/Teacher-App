from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from app.database.database import Base


class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    subject = Column(
        String,
        nullable=False
    )

    class_name = Column(
        String,
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=False
    )

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=False
    )