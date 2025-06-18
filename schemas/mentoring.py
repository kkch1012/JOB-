from pydantic import BaseModel
from datetime import datetime
from typing import List
from enum import Enum


# 1. 멘토링 상태 Enum 정의
class MentoringStatus(str, Enum):
    requested = 'requested'
    accepted = 'accepted'
    completed = 'completed'


# 2. 멘토링 생성 요청 스키마 (멘티는 로그인 사용자로 처리됨)
class MentoringCreate(BaseModel):
    mentor_id: int


# 3. 멘토링 상태 업데이트용 스키마
class MentoringUpdate(BaseModel):
    status: MentoringStatus


# 4. 멘토링 단일 응답용 스키마
class MentoringResponse(BaseModel):
    id: int
    mentor_id: int
    mentee_id: int
    date: datetime
    status: MentoringStatus

    class Config:
        orm_mode = True


# 5. 추천 멘토 응답용 스키마
class MentorResponse(BaseModel):
    id: int
    user_id: int
    career_years: int
    skills: List[str]  # 예: ['Python', 'Django']

    class Config:
        orm_mode = True
