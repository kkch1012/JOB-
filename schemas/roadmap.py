from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional


# 로드맵 항목 마스터 정보 (카탈로그)
class RoadmapItemBase(BaseModel):
    name: str
    type: str  # certificate, bootcamp, course 등
    description: Optional[str] = None


class RoadmapItemCreate(RoadmapItemBase):
    pass


class RoadmapItemResponse(RoadmapItemBase):
    id: int

    class Config:
        orm_mode = True


# 사용자별 RoadmapItem 상태 및 진척 정보
class UserRoadmapItemResponse(BaseModel):
    id: int
    start_date: Optional[date]
    end_date: Optional[date]
    status: str
    item: RoadmapItemResponse  # 마스터 정보 포함

    class Config:
        orm_mode = True


class RoadmapCreate(BaseModel):
    title: str
    description: Optional[str] = None
    job_role_id: Optional[int] = None
    items: List[int]  # item_id 리스트


class RoadmapResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    job_role_id: Optional[int]
    user_id: int
    created_at: datetime
    items: List[UserRoadmapItemResponse]

    class Config:
        orm_mode = True
