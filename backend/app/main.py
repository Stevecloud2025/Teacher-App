from fastapi import FastAPI

from app.database.database import Base, engine

from app.models.teacher import Teacher
from app.api.routes.teacher import router as teacher_router
from app.api.routes.lesson import router as lesson_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.quiz import router as quiz_router
from app.api.routes.question import router as question_router
from app.api.routes.option import router as option_router
from app.api.routes.attempt import router as attempt_router
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.option import QuizOption
from app.models.quiz_attempt import QuizAttempt
from app.api.routes.student import router as student_router
from app.models.quiz_attempt_answer import QuizAttemptAnswer
from app.models.student import Student


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Teacher Lesson Note API",
    version="1.0.0",
    description="Backend API for the Teacher Lesson Note Application"
)
app.include_router(teacher_router)
app.include_router(lesson_router)
app.include_router(dashboard_router)
app.include_router(quiz_router)
app.include_router(question_router)
app.include_router(option_router)
app.include_router(attempt_router)
app.include_router(student_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to the Teacher Lesson Note API!"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }