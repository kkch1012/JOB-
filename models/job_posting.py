from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  
    employment_type = Column(String, nullable=False) 
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)  # 회사 연결
    job_position = Column(String, nullable=False)
    posted_date = Column(Date, nullable=False)  
    deadline = Column(Date, nullable=False) 

    main_tasks = Column(Text, nullable=True)  
    qualifications = Column(Text, nullable=True)  
    preferences = Column(Text, nullable=True)  
    tech_stack = Column(Text, nullable=True) 

    company = relationship("Company", backref="job_postings")
    def company_name(self):
        return self.company.name