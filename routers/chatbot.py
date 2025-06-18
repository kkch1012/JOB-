from fastapi import APIRouter, Body
from services.chatbot.dispatcher import dispatch_chat

router = APIRouter(tags=["Chatbot"])

@router.post("/ask", summary="챗봇 질문 응답", description="사용자의 자연어 질문에 대한 챗봇 응답을 반환합니다.")
def ask_chatbot(message: str = Body(..., embed=True)):
    """
    사용자의 메시지를 받아 적절한 핸들러로 분기하고 응답을 생성합니다.
    """
    response = dispatch_chat(message)
    return {"response": response}
