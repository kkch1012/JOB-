from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import DATABASE_URL  # ✅ .env에서 불러온 DB 경로 사용

# DB 연결 설정
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 및 베이스 설정
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# 의존성 주입용 DB 세션 생성 함수
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
