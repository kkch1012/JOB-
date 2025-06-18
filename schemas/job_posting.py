from pydantic import BaseModel
from datetime import date
from typing import Optional

class JobPostingResponse(BaseModel):
    id: int
    title: str
    employment_type: Optional[str]  
    applicant_type: str             
    job_position: str
    posted_date: date
    deadline: date
    main_tasks: Optional[str]
    qualifications: Optional[str]
    preferences: Optional[str]
    tech_stack: Optional[str]
    company_name: str

    class Config:
        orm_mode = True

class JobPostingCreate(BaseModel):
    title: str
    employment_type: Optional[str] = None  
    applicant_type: str
    company_id: int
    job_position: str
    posted_date: date
    deadline: date
    main_tasks: Optional[str] = None
    qualifications: Optional[str] = None
    preferences: Optional[str] = None
    tech_stack: Optional[str] = None
