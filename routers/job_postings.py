from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.job_posting import JobPosting
from models.company import Company
from database import get_db
from schemas.job_posting import JobPostingResponse
from sqlalchemy import or_

router = APIRouter(tags=["JobPostings"])

@router.get("/search", response_model=List[JobPostingResponse])
def search_job_postings(
    company_name: Optional[str] = Query(None),
    employment_type: Optional[str] = Query(None),
    job_position: Optional[str] = Query(None),
    tech_keyword: Optional[str] = Query(None),  # 기술스택 키워드
    db: Session = Depends(get_db)
):
    query = db.query(JobPosting).join(Company)

    if company_name:
        query = query.filter(Company.name.ilike(f"%{company_name}%"))
    if employment_type:
        query = query.filter(JobPosting.employment_type.ilike(f"%{employment_type}%"))
    if job_position:
        query = query.filter(JobPosting.job_position.ilike(f"%{job_position}%"))
    if tech_keyword:
        query = query.filter(JobPosting.tech_stack.ilike(f"%{tech_keyword}%"))

    return query.all()
