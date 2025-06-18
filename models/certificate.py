from sqlalchemy import Column, Integer, String
from database import Base

class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)          
    issuer = Column(String, nullable=False)        # 발급 기관
