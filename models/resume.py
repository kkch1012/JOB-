from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float, Date
from sqlalchemy.orm import relationship
from database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    university = Column(String, nullable=True)
    major = Column(String, nullable=True)
    gpa = Column(Float, nullable=True)
    education_status = Column(String, nullable=True)
    degree = Column(String, nullable=False)
    language_score = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    desired_job = Column(String, nullable=True)

    user = relationship("User", back_populates="resume")

    certificates = relationship(
        "UserCertificate",
        back_populates="resume",
        cascade="all, delete-orphan"
    )

    skills = relationship(
        "UserSkill",
        back_populates="resume",
        cascade="all, delete-orphan"
    )


class UserCertificate(Base):
    __tablename__ = 'user_certificates'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    certificate_id = Column(Integer, ForeignKey("certificates.id", ondelete="CASCADE"), nullable=False)
    acquired_date = Column(Date, nullable=False)

    resume = relationship("Resume", back_populates="certificates")
    certificate = relationship("Certificate")


class UserSkill(Base):
    __tablename__ = 'user_skills'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency = Column(String, nullable=True)  # 예: beginner, intermediate, expert

    resume = relationship("Resume", back_populates="skills")
    skill = relationship("Skill")
