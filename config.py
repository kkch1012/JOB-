from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일 로드

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
DATABASE_URL = os.getenv("DATABASE_URL")

print("[DEBUG] SECRET_KEY:", SECRET_KEY)
print("[DEBUG] ALGORITHM:", ALGORITHM)
print("[DEBUG] ACCESS_TOKEN_EXPIRE_MINUTES:", ACCESS_TOKEN_EXPIRE_MINUTES)
