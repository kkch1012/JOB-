from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserSkillResponse(BaseModel):
    id: int
    skill_id: int
    skill_name: Optional[str]
    proficiency: Optional[str]

    class Config:
        from_attributes = True

class UserCertificateResponse(BaseModel):
    id: int
    certificate_id: int
    certificate_name: Optional[str]
    acquired_date: date

    class Config:
        from_attributes = True

class ResumeBase(BaseModel):
    desired_job: Optional[str] = None
    university: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[float] = None
    education_status: Optional[str] = None
    degree: str
    language_score: Optional[str] = None
    experience: Optional[str] = None

class ResumeCertificateInput(BaseModel):
    certificate_id: int
    acquired_date: date

class ResumeSkillInput(BaseModel):
    skill_id: int
    proficiency: Optional[str] = None

class ResumeCreate(ResumeBase):
    skills: Optional[List[ResumeSkillInput]] = None
    certificates: Optional[List[ResumeCertificateInput]] = None 

class ResumeUpdate(ResumeBase):
    skills: Optional[List[ResumeSkillInput]] = None
    certificates: Optional[List[ResumeCertificateInput]] = None 

class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    skills: List[UserSkillResponse] = []
    certificates: List[UserCertificateResponse] = []

    class Config:
        from_attributes = True
