from pydantic import BaseModel, Field
from typing import Optional, List

class ResumeUpdate(BaseModel):
    age: Optional[int] = Field(None, description="나이")
    desired_job: Optional[str] = Field(None, description="희망 직무")
    university: Optional[str] = Field(None, description="대학교")
    major: Optional[str] = Field(None, description="전공 학과")
    gpa: Optional[float] = Field(None, description="학점 (예: 4.2)")
    skills: Optional[List[str]] = Field(default_factory=list, description="보유 기술 목록")
    certificates: Optional[List[str]] = Field(default_factory=list, description="보유 자격증 목록")
    experiences: Optional[List[str]] = Field(default_factory=list, description="인턴/프로젝트 등 경험")
    educations: Optional[List[str]] = Field(default_factory=list, description="수강한 교육 및 부트캠프 등")
