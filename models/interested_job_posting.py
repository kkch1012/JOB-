from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class InterestedJobPosting(Base):
    __tablename__ = "interested_job_postings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    job_posting_cleaned_id = Column(Integer, ForeignKey("job_postings_cleaned.id"), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="interested_jobs")

    cleaned_job_posting = relationship("JobPostingCleaned", back_populates="interested_users")
