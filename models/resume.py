from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    age = Column(Integer, nullable=True)
    skills = Column(JSON, nullable=True)
    university = Column(String, nullable=True)
    major = Column(String, nullable=True)
    gpa = Column(Float, nullable=True)
    education_status = Column(String, nullable=True)
    degree = Column(String, nullable=True)
    language_score = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    certificates = Column(JSON, nullable=True)
    desired_job = Column(String, nullable=True)

    user = relationship("User", back_populates="resume")
