from fastapi import APIRouter

router = APIRouter()

@router.get("/",summary="공고 추천 결과", description="추천 공고 결과 리스트를 반환합니다.")
def get_recommendations():
    return {"message": "추천 결과 리스트 반환 예정"}
