from pydantic import BaseModel, EmailStr
from typing import Optional
from schemas.resume import ResumeResponse
from datetime import date   

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    phone_number: Optional[str] = None

class ProfileResponse(BaseModel):
    name: str
    gender: Optional[str] = None
    birth_date: Optional[str] = None 
    phone_number: Optional[date] = None

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
