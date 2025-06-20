from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse
from models.resume import Resume, UserSkill, UserCertificate
from models.user import User
from models.skill import Skill
from models.certificate import Certificate
from utils.dependencies import get_current_user
from database import get_db
from datetime import date

router = APIRouter(tags=["Resume"])


@router.get("/me", response_model=ResumeResponse, summary="내 이력서 조회")
def get_my_resume(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).options(
        joinedload(User.resume)
        .joinedload(Resume.skills)
        .joinedload(UserSkill.skill),
        joinedload(User.resume)
        .joinedload(Resume.certificates)
        .joinedload(UserCertificate.certificate)
    ).filter(User.email == current_user_email).first()

    if not user or not user.resume:
        raise HTTPException(status_code=404, detail="이력서를 찾을 수 없습니다.")

    return user.resume


@router.put("/me", response_model=ResumeResponse, summary="내 이력서 등록/수정")
def update_my_resume(
    resume_data: ResumeUpdate,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).options(joinedload(User.resume)).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    if user.resume:
        resume = user.resume
        for key, value in resume_data.dict(exclude_unset=True, exclude={"skills", "certificates"}).items():
            setattr(resume, key, value)
    else:
        resume = Resume(**resume_data.dict(exclude_unset=True, exclude={"skills", "certificates"}), user_id=user.id)
        db.add(resume)
        db.flush()

    if resume_data.skills is not None:
        db.query(UserSkill).filter(UserSkill.resume_id == resume.id).delete()
        for skill_input in resume_data.skills:
            db.add(UserSkill(
                resume_id=resume.id,
                skill_id=skill_input.skill_id,
                proficiency=skill_input.proficiency
            ))

    if resume_data.certificates is not None:
        db.query(UserCertificate).filter(UserCertificate.resume_id == resume.id).delete()
        for cert in resume_data.certificates:
            db.add(UserCertificate(
                resume_id=resume.id,
                certificate_id=cert.certificate_id,
                acquired_date=cert.acquired_date
            ))

    db.commit()
    db.refresh(resume)
    return resume
