from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    required_skills = relationship("JobRequiredSkill", back_populates="job_role", cascade="all, delete-orphan")
    postings = relationship("JobPostingCleaned", back_populates="job_role", cascade="all, delete-orphan")
