from fastapi import FastAPI

from app.database.database import Base, engine

from app.models.teacher import Teacher
from app.api.routes.teacher import router as teacher_router
from app.api.routes.lesson import router as lesson_router
from app.api.routes.dashboard import router as dashboard_router
from app.models.lesson import Lesson

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Teacher Lesson Note API",
    version="1.0.0",
    description="Backend API for the Teacher Lesson Note Application"
)
app.include_router(teacher_router)
app.include_router(lesson_router)
app.include_router(dashboard_router)


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