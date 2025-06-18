from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User
from models.interested_job_posting import InterestedJobPosting
from models.job_postings_cleaned import JobPostingCleaned
from schemas.interested_job_posting import InterestedJobCreate, InterestedJobResponse
from utils.dependencies import get_current_user

router = APIRouter(tags=["Interests"])

@router.post("/", response_model=InterestedJobResponse, summary="관심 공고 등록")
def create_interested_job(
    interest: InterestedJobCreate,
    db: Session = Depends(get_db),
    current_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(InterestedJobPosting).filter_by(
        user_id=user.id,
        job_posting_id=interest.job_posting_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 관심공고에 등록됨")

    new_interest = InterestedJobPosting(
        user_id=user.id,
        job_posting_id=interest.job_posting_id
    )
    db.add(new_interest)
    db.commit()
    db.refresh(new_interest)
    return new_interest


@router.get("/", response_model=List[InterestedJobResponse], summary="사용자의 관심 공고 ID 목록 조회")
def get_user_interests(
    db: Session = Depends(get_db),
    current_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(InterestedJobPosting)\
        .filter(InterestedJobPosting.user_id == user.id)\
        .order_by(InterestedJobPosting.created_at.desc())\
        .all()


@router.get("/details", response_model=List[InterestedJobResponse], summary="관심 공고 상세 조회")
def get_interested_jobs_details(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(InterestedJobPosting)
        .join(InterestedJobPosting.cleaned_job_posting)
        .join(JobPostingCleaned.company)
        .filter(InterestedJobPosting.user_id == current_user.id)
        .order_by(InterestedJobPosting.created_at.desc())
        .all()
    )


@router.delete("/{interest_id}", status_code=204, summary="관심 공고 삭제")
def delete_interested_job(
    interest_id: int,
    db: Session = Depends(get_db),
    current_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    interest = db.query(InterestedJobPosting).filter_by(
        id=interest_id,
        user_id=user.id
    ).first()
    if not interest:
        raise HTTPException(status_code=404, detail="관심공고를 찾을 수 없음")

    db.delete(interest)
    db.commit()
