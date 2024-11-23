from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from ..db.database import Base


class TargetUrl(Base):
    __tablename__ = "target_url"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String)
    path = Column(String)
    params = Column(String)
    is_deleted = Column(Boolean, default=False)
    created_date = Column(DateTime(timezone=True), default=func.now())
    updated_date = Column(DateTime(timezone=True),
                          server_onupdate=func.now())
