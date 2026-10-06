from pydantic import BaseModel


class PerformanceSummaryResponse(BaseModel):
    student_id: int

    quiz_average: float
    quiz_count: int

    homework_average: float
    graded_homework_count: int

    attendance_percentage: float
    attendance_total: int
    present_count: int
    late_count: int
    absent_count: int