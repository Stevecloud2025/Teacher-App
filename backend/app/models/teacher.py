from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False, index=True)

    phone = Column(String(20), nullable=True)

    password = Column(String(255), nullable=False)

    school_name = Column(String(150), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lessons = relationship("Lesson", back_populates="teacher")