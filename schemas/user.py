from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from schemas.resume import ResumeResponse
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str = Field(..., exclude=True)
    name: str
    gender: Optional[str] = None
    birth_date: date
    phone_number: str

    @model_validator(mode="after")
    def passwords_match(self) -> 'UserCreate':
        if self.password != self.confirm_password:
            raise ValueError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return self

class ProfileResponse(BaseModel):
    name: str
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True

class UserProfileResponse(BaseModel):
    email: EmailStr
    profile: Optional[ProfileResponse] = None
    resume: Optional[ResumeResponse] = None

    class Config:
        orm_mode = True

class CommunityComparisonResponse(BaseModel):
    desired_job: str
    user_count: int
    average_age: float
    average_certificates: float
