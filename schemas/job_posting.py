from pydantic import BaseModel
from datetime import date
from typing import Optional

class JobPostingResponse(BaseModel):
    id: int
    title: str
    employment_type: str
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
