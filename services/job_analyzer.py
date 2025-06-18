# 공고 전처리

from sqlalchemy.orm import Session
from models.job_posting import JobPosting
from models.job_postings_cleaned import JobPostingCleaned
from models.job_required_skill import JobRequiredSkill
from utils.text_processing import extract_required_skills, extract_preferred_skills, classify_job_role  # 전처리 유틸 가정

def analyze_and_save_cleaned_postings(db: Session):
    postings = db.query(JobPosting).all()

    for post in postings:
        # --- 예시 전처리 ---
        main_tasks = post.description or ""
        qualifications = post.qualifications or ""
        preferences = post.preferences or ""

        # 직무 자동 분류 (예시)
        job_role_id = classify_job_role(main_tasks + qualifications)

        # 기술스택 추출
        required_skills = extract_required_skills(qualifications)
        preferred_skills = extract_preferred_skills(preferences)

        # 중복 방지: 기존 분석된 공고 있는지 체크
        exists = db.query(JobPostingCleaned).filter_by(original_posting_id=post.id).first()
        if exists:
            continue

        cleaned = JobPostingCleaned(
            original_posting_id=post.id,
            job_role_id=job_role_id,
            title=post.title,
            employment_type=post.employment_type,
            company_id=post.company_id,
            job_position=post.job_position,
            posted_date=post.posted_date,
            deadline=post.deadline,
            main_tasks=main_tasks,
            qualifications=qualifications,
            preferences=preferences,
            required_skills=", ".join(required_skills),
            preferred_skills=", ".join(preferred_skills),
        )
        db.add(cleaned)

    db.commit()
