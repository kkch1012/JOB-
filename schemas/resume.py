# schemas/resume.py
from pydantic import BaseModel
from typing import List, Optional

class ResumeBase(BaseModel):
    age: Optional[int] = None
    skills: Optional[List[str]] = None 
    university: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[float] = None
    education_status: Optional[str] = None  
    experience: Optional[str] = None
    certificates: Optional[List[str]] = None
    desired_job: Optional[str] = None
    
class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: int

    class Config:
        orm_mode = True
