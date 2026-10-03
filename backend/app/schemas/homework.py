from datetime import date
from pydantic import BaseModel


class HomeworkCreate(BaseModel):
    title: str
    description: str
    subject: str
    class_name: str
    due_date: date


class HomeworkResponse(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    class_name: str
    due_date: date
    teacher_id: int

    class Config:
        from_attributes = True