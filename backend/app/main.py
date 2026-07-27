from fastapi import FastAPI

app = FastAPI(
    title="Teacher Lesson Note API",
    version="1.0.0",
    description="Backend API for the Teacher Lesson Note Application"
)

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