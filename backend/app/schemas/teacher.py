from pydantic import BaseModel, EmailStr


class TeacherCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    school_name: str


class TeacherLogin(BaseModel):
    email: EmailStr
    password: str


class TeacherResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    school_name: str


class LoginResponse(BaseModel):
    message: str
    teacher_id: int
    full_name: str
    email: EmailStr
    access_token: str


class TeacherProfileResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str | None = None
    school_name: str | None = None

    class Config:
        from_attributes = True

class TeacherProfileUpdate(BaseModel):
    full_name: str
    phone: str | None = None
    school_name: str | None = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str