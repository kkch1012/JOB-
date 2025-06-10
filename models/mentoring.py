from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Mentor(Base):
    __tablename__ = 'mentors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    skills = Column(String)
    career_years = Column(Integer)

class Mentoring(Base):
    __tablename__ = 'mentoring'
    id = Column(Integer, primary_key=True)
    mentor_id = Column(Integer, ForeignKey('mentors.id'))
    mentee_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='requested')  # requested, accepted, completed
