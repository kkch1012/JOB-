from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.skill import Skill
from schemas.skill import SkillResponse
from typing import List

router = APIRouter(tags=["Skills"])

# 스킬 목록 조회
@router.get("/", response_model=List[SkillResponse], summary="스킬 목록 조회")
def get_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()

# 스킬 생성
@router.post("/", response_model=SkillResponse, summary="스킬 생성")
def create_skill(name: str, db: Session = Depends(get_db)):
    if db.query(Skill).filter(Skill.name == name).first():
        raise HTTPException(status_code=400, detail="이미 존재하는 스킬입니다.")
    skill = Skill(name=name)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill
