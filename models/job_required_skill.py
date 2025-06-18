# models/job_required_skill.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class JobRequiredSkill(Base):
    __tablename__ = "job_required_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_role_id = Column(Integer, ForeignKey("job_roles.id", ondelete="CASCADE"), nullable=False)
    skill = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "required" or "preferred"

    job_role = relationship("JobRole", back_populates="required_skills")
