from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db
from models.mentoring import Mentor, Mentoring, MentorSkill
from models.user import User
from models.skill import Skill
from schemas.mentoring import (
    MentoringCreate, MentoringUpdate,
    MentoringResponse, MentorResponse, MentoringStatus
)
from utils.dependencies import get_current_user

router = APIRouter(tags=["Mentoring"])


# 1. 멘토링 요청 생성
@router.post("/", response_model=MentoringResponse, summary="멘토링 요청 생성")
def create_mentoring(
    request: MentoringCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 존재하는 멘토 확인
    mentor = db.query(Mentor).filter(Mentor.id == request.mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    # 멘토링 생성
    mentoring = Mentoring(
        mentor_id=request.mentor_id,
        mentee_id=current_user.id,
        date=datetime.now(),
        status="requested"
    )
    db.add(mentoring)
    db.commit()
    db.refresh(mentoring)
    return mentoring


# 2. 멘토링 상태 업데이트
@router.patch("/{mentoring_id}", response_model=MentoringResponse, summary="멘토링 상태 업데이트")
def update_mentoring_status(
    mentoring_id: int,
    update: MentoringUpdate,
    db: Session = Depends(get_db)
):
    mentoring = db.query(Mentoring).filter(Mentoring.id == mentoring_id).first()
    if not mentoring:
        raise HTTPException(status_code=404, detail="Mentoring not found")

    mentoring.status = update.status
    db.commit()
    db.refresh(mentoring)
    return mentoring


# 3. 추천 멘토 조회
@router.get("/recommend", response_model=List[MentorResponse], summary="멘토 추천 조회")
def recommend_mentors(
    skill: Optional[str] = Query(None, description="필요한 기술"),
    min_years: Optional[int] = Query(None, description="최소 경력"),
    db: Session = Depends(get_db)
):
    query = db.query(Mentor)

    if min_years is not None:
        query = query.filter(Mentor.career_years >= min_years)

    mentors = query.all()
    result = []

    for mentor in mentors:
        mentor_skills = [
            ms.skill.name for ms in mentor.skills if not skill or skill.lower() in ms.skill.name.lower()
        ]
        if skill is None or mentor_skills:
            result.append(MentorResponse(
                id=mentor.id,
                user_id=mentor.user_id,
                career_years=mentor.career_years,
                skills=mentor_skills
            ))

    return result
