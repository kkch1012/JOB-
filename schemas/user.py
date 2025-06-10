# schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from schemas.resume import ResumeResponse

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserProfileResponse(BaseModel):
    email: EmailStr
    name: str
    resume: Optional[ResumeResponse] = None

    class Config:
        orm_mode = True

class CommunityComparisonResponse(BaseModel):
    desired_job: str
    user_count: int
    average_age: float
    average_certificates: float
