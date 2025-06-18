from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from schemas.user import UserProfileResponse, CommunityComparisonResponse
from models.user import User
from models.resume import Resume
from utils.dependencies import get_current_user
from database import get_db

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserProfileResponse, summary="내 정보 조회")
def get_my_profile(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User)\
        .options(joinedload(User.profile))\
        .filter(User.email == current_user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return user


@router.get("/compare", response_model=CommunityComparisonResponse, summary="사용자 비교")
def compare_users_by_job(desired_job: str, db: Session = Depends(get_db)):
    resumes = (
        db.query(Resume)
        .join(User)
        .filter(Resume.desired_job == desired_job)
        .all()
    )

    if not resumes:
        raise HTTPException(status_code=404, detail="해당 희망 직무를 가진 이력서가 없습니다.")

    total_age = 0
    total_certificates = 0
    count = 0

    for resume in resumes:
        age = resume.age
        certificates = resume.certificates or []

        if age is not None:
            total_age += age
            total_certificates += len(certificates)
            count += 1

    if count == 0:
        raise HTTPException(status_code=404, detail="평균을 계산할 수 있는 사용자 정보가 없습니다.")

    return CommunityComparisonResponse(
        desired_job=desired_job,
        user_count=count,
        average_age=round(total_age / count, 1),
        average_certificates=round(total_certificates / count, 2)
    )
