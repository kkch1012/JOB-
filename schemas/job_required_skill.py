from pydantic import BaseModel
from typing import Optional

class JobRequiredSkillCreate(BaseModel):
    job_role_id: int
    skill: str
    type: str  # "required" or "preferred"

class JobRequiredSkillResponse(BaseModel):
    id: int
    job_role_id: int
    skill: str
    type: str

    class Config:
        orm_mode = True
