from pydantic import BaseModel


class StudentCreate(BaseModel):
    full_name: str
    email: str
    password: str
    school_name: str | None = None
    class_name: str | None = None


class StudentResponse(BaseModel):
    id: int
    full_name: str
    email: str
    school_name: str | None
    class_name: str | None

    class Config:
        from_attributes = True

        from pydantic import BaseModel


class StudentCreate(BaseModel):
    full_name: str
    email: str
    password: str
    school_name: str | None = None
    class_name: str | None = None


class StudentResponse(BaseModel):
    id: int
    full_name: str
    email: str
    school_name: str | None
    class_name: str | None

    class Config:
        from_attributes = True


class StudentLogin(BaseModel):
    email: str
    password: str