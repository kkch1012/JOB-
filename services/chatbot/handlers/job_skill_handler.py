# 공고 관련 질문 처리

from ..llm_wrapper import ask_llm
from ..prompt_templates import job_skill_prompt

def handle(message: str) -> str:
    
    return ask_llm(job_skill_prompt(message))