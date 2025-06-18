from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class Mentor(Base):
    __tablename__ = 'mentors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    career_years = Column(Integer, nullable=True)

    skills = relationship("MentorSkill", back_populates="mentor", cascade="all, delete-orphan")

class Mentoring(Base):
    __tablename__ = 'mentoring'
    id = Column(Integer, primary_key=True)
    mentor_id = Column(Integer, ForeignKey('mentors.id'), nullable=False)
    mentee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default='requested')  # requested, accepted, completed

class MentorSkill(Base):
    __tablename__ = 'mentor_skills'
    id = Column(Integer, primary_key=True)
    mentor_id = Column(Integer, ForeignKey('mentors.id', ondelete='CASCADE'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)

    mentor = relationship("Mentor", back_populates="skills")
    skill = relationship("Skill")
