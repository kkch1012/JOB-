# 사용자 질문 -> 처리 모듈 라우팅

def dispatch_chat(message: str):
    if "공고" in message and "기술" in message:
        from .handlers.job_skill_handler import handle
        return handle(message)
    elif "로드맵" in message:
        from .handlers.roadmap_handler import handle
        return handle(message)
    elif "이력서" in message and "비교" in message:
        from .handlers.resume_match_handler import handle
        return handle(message)
    elif "스터디" in message or "커뮤니티" in message:
        from .handlers.community_handler import handle
        return handle(message)
    else:
        from .handlers.default_handler import handle
        return handle(message)