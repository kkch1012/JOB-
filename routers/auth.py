from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, UserProfile
from utils.schemas import LoginRequest, TokenResponse
from schemas.user import UserCreate
from utils.dependencies import get_current_user
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone 
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # ← 수정
    to_encode.update({"exp": expire, "sub": data["email"]})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=TokenResponse, summary="회원가입 요청", description="이메일과 비밀번호를 이용하여 새 사용자를 등록합니다.")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 비밀번호 해싱 및 유저 생성
    hashed = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 프로필 생성
    new_profile = UserProfile(
        user_id=new_user.id,
        name=user.name,
        gender=user.gender,
        birth_date=user.birth_date,
        phone_number=user.phone_number
    )
    db.add(new_profile)
    db.commit()

    token = create_access_token({"email": new_user.email})
    return {"access_token": token, "token_type": "bearer"}



@router.delete("/delete", summary="계정 탈퇴", description="사용자의 계정을 삭제합니다.")
def delete_account(
    db: Session = Depends(get_db),
    current_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "계정이 삭제되었습니다."}


@router.post("/login", response_model=TokenResponse, summary="로그인 요청", description="이메일과 비밀번호를 이용하여 로그인합니다.")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"email": user.email})
    return {"access_token": token, "token_type": "bearer"}
