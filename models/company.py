from sqlalchemy import Column, Integer, String
from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    size = Column(String, nullable=False)  
    address = Column(String, nullable=True)  
