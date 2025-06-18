# 로드맵/추천 관련 질문

from ..llm_wrapper import ask_llm
from ..prompt_templates import roadmap_prompt

def handle(message: str) -> str:
    return ask_llm(roadmap_prompt(message))