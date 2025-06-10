from fastapi import APIRouter

router = APIRouter()

@router.get("/",summary="로드맵 조회", description="전체 로드맵 조회")
def get_roadmap():
    return {"message": "로드맵 조회 또는 결과 반환 예정"}

@router.post("/generate",summary="로드맵 생성", description="이력서를 기반으로 로드맵을 생성합니다.")
def generate_roadmap():
    return {"message": "이력서를 기반으로 로드맵 생성 예정"}

@router.post("/compare",summary="이력서와 공고 비교", description="이력서와 채용공고 간의 차이를 분석합니다.")
def compare_resume_and_job():
    return {"message": "이력서와 공고 간 차이 분석 예정"}

@router.get("/learn", summary="학습 자료 추천", description="기술 격차에 따른 학습 자료를 추천합니다.")
def get_learning_resources():
    return {"message": "기술 격차에 따른 학습 자료 추천 예정"}
