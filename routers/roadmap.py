from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timezone

from database import get_db
from models.roadmap import Roadmap, RoadmapItem, UserRoadmapItem
from models.user import User
from models.resume import Resume, UserSkill
from schemas.roadmap import RoadmapCreate, RoadmapResponse
from utils.dependencies import get_current_user

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])


# 전체 로드맵 조회 (관리자/개발용)
@router.get("/", summary="전체 로드맵 조회", response_model=List[RoadmapResponse])
def get_roadmap(db: Session = Depends(get_db)):
    return db.query(Roadmap).options(joinedload(Roadmap.items).joinedload(UserRoadmapItem.item)).all()


# 유저 이력서를 기반으로 로드맵 생성
@router.post("/generate", summary="이력서 기반 로드맵 생성", response_model=RoadmapResponse)
def generate_roadmap(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).options(joinedload(User.resume).joinedload(Resume.skills)).filter(User.email == current_user_email).first()
    if not user or not user.resume:
        raise HTTPException(status_code=404, detail="이력서를 찾을 수 없습니다.")

    user_skill_ids = {us.skill_id for us in user.resume.skills}

    # 예시: 추천하고 싶은 기술 항목 ID 하드코딩 또는 추후 모델 기반 추론 가능
    recommended_items = db.query(RoadmapItem).filter(RoadmapItem.name.in_(["AWS 자격증", "딥러닝 부트캠프"])).all()

    roadmap = Roadmap(
        user_id=user.id,
        title="이력서 기반 자동 로드맵",
        description="이력서 분석을 통해 부족한 기술 보완",
        created_at=datetime.now(timezone.utc)
    )
    db.add(roadmap)
    db.flush()

    for item in recommended_items:
        db.add(UserRoadmapItem(
            roadmap_id=roadmap.id,
            item_id=item.id,
            status="planned"
        ))

    db.commit()
    db.refresh(roadmap)
    return roadmap


# 기술 격차 기반 학습 자료 추천
@router.get("/learn", summary="학습 자료 추천", description="기술 격차에 따른 학습 자료를 추천합니다.")
def get_learning_resources():
    return {
        "message": "기술 격차 기반 학습 자료 추천",
        "recommendations": [
            {"title": "FastAPI 실습 강의", "platform": "Inflearn"},
            {"title": "Docker 실전 입문", "platform": "Udemy"},
        ]
    }
