from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.interested_job_posting import InterestedJobPosting

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    resume = relationship("Resume", uselist=False, back_populates="user")
    profile = relationship("UserProfile", uselist=False, back_populates="user") 

    interested_jobs = relationship(
        InterestedJobPosting,
        back_populates="user",
        cascade="all, delete-orphan"
    )


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    name = Column(String, nullable=False)        
    gender = Column(String, nullable=True)        
    birth_date = Column(Date, nullable=True)      
    phone_number = Column(String, nullable=True)  

    user = relationship("User", back_populates="profile")
