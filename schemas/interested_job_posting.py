from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InterestedJobCreate(BaseModel):
    job_posting_cleaned_id: int


class InterestedJobResponse(BaseModel):
    id: int
    job_posting_cleaned_id: int
    created_at: datetime

    title: str
    employment_type: str
    job_position: str
    posted_date: datetime
    deadline: datetime
    company_name: str
    job_role_name: Optional[str] = None
    required_skills: Optional[str] = None
    preferred_skills: Optional[str] = None

    class Config:
        orm_mode = True
