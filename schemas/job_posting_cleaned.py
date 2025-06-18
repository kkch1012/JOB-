from pydantic import BaseModel
from datetime import date
from typing import Optional

class JobPostingCleanedResponse(BaseModel):
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

    required_skills: Optional[str]
    preferred_skills: Optional[str]

    job_role_id: Optional[int]
    job_role_name: Optional[str]

    company_id: int
    company_name: str

    class Config:
        orm_mode = True
