from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    subject = Column(String, nullable=False)

    class_name = Column(String, nullable=False)

    topic = Column(String, nullable=False)

    content = Column(Text, nullable=False)

    status = Column(String, nullable=False, default="draft")


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=False
    )

    teacher = relationship("Teacher", back_populates="lessons")