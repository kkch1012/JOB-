# utils/text_processing.py

def extract_required_skills(text: str) -> list:
    keywords = ["Python", "SQL", "FastAPI", "Django"]
    return [kw for kw in keywords if kw.lower() in text.lower()]

def extract_preferred_skills(text: str) -> list:
    keywords = ["AWS", "Docker", "Kubernetes", "GraphQL"]
    return [kw for kw in keywords if kw.lower() in text.lower()]

def classify_job_role(text: str) -> int:
    if "데이터" in text:
        return 1  # 예: Data Analyst
    elif "백엔드" in text or "서버" in text:
        return 2  # 예: Backend Developer
    return 99  # Unknown
