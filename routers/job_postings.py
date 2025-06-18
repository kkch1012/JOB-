from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.job_posting import JobPosting
from models.company import Company
from database import get_db
from schemas.job_posting import JobPostingResponse, JobPostingCreate

router = APIRouter()

@router.post("/", summary="채용공고 등록")
def create_job_posting(
    job_data: JobPostingCreate,
    db: Session = Depends(get_db)
):
    new_posting = JobPosting(**job_data.dict())
    db.add(new_posting)
    db.commit()
    db.refresh(new_posting)
    return {"message": "채용공고 등록 완료", "id": new_posting.id}

@router.get("/search", response_model=List[JobPostingResponse], summary="채용 공고 검색")
def search_job_postings(
    company_name: Optional[str] = Query(None, description="회사 이름"),
    company_size: Optional[str] = Query(None, description="회사 규모 (대기업, 중견기업, 중소기업)"),
    employment_type: Optional[str] = Query(None, description="고용 형태"),
    job_position: Optional[str] = Query(None, description="직무명"),
    tech_keyword: Optional[str] = Query(None, description="기술 스택 키워드"),
    sort: Optional[str] = Query(None, description="정렬 방식: latest(최신순), deadline(마감순)"),
    db: Session = Depends(get_db)
):
    query = db.query(JobPosting).join(Company)

    if company_name:
        query = query.filter(Company.name.ilike(f"%{company_name}%"))
    if company_size:
        query = query.filter(Company.size == company_size)
    if employment_type:
        query = query.filter(JobPosting.employment_type.ilike(f"%{employment_type}%"))
    if job_position:
        query = query.filter(JobPosting.job_position.ilike(f"%{job_position}%"))
    if tech_keyword:
        query = query.filter(JobPosting.tech_stack.ilike(f"%{tech_keyword}%"))

    if sort == "latest":
        query = query.order_by(JobPosting.posted_date.desc())
    elif sort == "deadline":
        query = query.order_by(JobPosting.deadline.asc())
    else:
        query = query.order_by(JobPosting.posted_date.desc())

    return query.all()

