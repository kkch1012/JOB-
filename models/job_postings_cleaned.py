from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class JobPostingCleaned(Base):
    __tablename__ = "job_postings_cleaned"

    id = Column(Integer, primary_key=True, index=True)

    original_posting_id = Column(Integer, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)

    job_role_id = Column(Integer, ForeignKey("job_roles.id", ondelete="SET NULL"), nullable=True)
    job_role_name = Column(String, nullable=True)

    title = Column(String, nullable=False)
    employment_type = Column(String, nullable=True) 
    applicant_type = Column(String, nullable=False)  

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    job_position = Column(String, nullable=False)
    posted_date = Column(Date, nullable=False)
    deadline = Column(Date, nullable=False)

    main_tasks = Column(Text, nullable=True)
    qualifications = Column(Text, nullable=True)
    preferences = Column(Text, nullable=True)

    required_skills = Column(Text, nullable=True)
    preferred_skills = Column(Text, nullable=True)

    company = relationship("Company", backref="cleaned_postings")
    original_posting = relationship("JobPosting")

    job_role = relationship("JobRole", back_populates="postings")

    interested_users = relationship(
        "InterestedJobPosting",
        back_populates="cleaned_job_posting",
        cascade="all, delete-orphan"
    )
