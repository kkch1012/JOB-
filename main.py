from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import Base, engine, SessionLocal
from models import job_required_skill, job_posting, job_postings_cleaned  # 필요한 모든 모델 import
from services.job_analyzer import analyze_and_save_cleaned_postings

# 라우터 import
from routers import (
    auth,
    users,
    job_postings,
    recommend,
    roadmap,
    community,
    interests,
    chatbot,
    mentoring,
    resume,
    skill  
)

# 앱 초기화 시 실행할 작업
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        analyze_and_save_cleaned_postings(db)  # 공고 전처리 자동 실행
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(job_postings.router, prefix="/jobs", tags=["Jobs"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
app.include_router(roadmap.router, prefix="/roadmap", tags=["Roadmap"])
app.include_router(community.router, prefix="/community", tags=["Community"])
app.include_router(interests.router, prefix="/interests", tags=["Interests"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(mentoring.router, prefix="/mentoring", tags=["Mentoring"])
app.include_router(resume.router, prefix="/resume", tags=["Resume"])   
app.include_router(skill.router, prefix="/skills", tags=["Skills"])    