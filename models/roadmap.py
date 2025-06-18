from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)             # 예: 정보처리기사
    type = Column(String, nullable=False)             # "certificate", "bootcamp", "course"
    description = Column(Text, nullable=True)


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    job_role_id = Column(Integer, ForeignKey("job_roles.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="roadmaps")
    job_role = relationship("JobRole", backref="roadmaps")
    items = relationship("UserRoadmapItem", back_populates="roadmap", cascade="all, delete-orphan")


class UserRoadmapItem(Base):
    __tablename__ = "user_roadmap_items"

    id = Column(Integer, primary_key=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("roadmap_items.id", ondelete="CASCADE"), nullable=False)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String, nullable=False, default="planned")  # planned, in_progress, completed 등

    roadmap = relationship("Roadmap", back_populates="items")
    item = relationship("RoadmapItem")
