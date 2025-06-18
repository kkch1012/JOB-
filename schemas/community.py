from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    author_email: str
    created_at: datetime

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    desired_job_id: Optional[int] = None 
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    desired_job_id: Optional[int] = None
    title: str
    content: str
    author_email: str
    created_at: datetime
    comments: List[CommentResponse] = []

    class Config:
        orm_mode = True
